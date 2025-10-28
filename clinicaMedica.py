import sqlite3
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox

DB_FILE = "clinica.db"


# Funciones de base de datos

def ejecutar(query, params=()):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        return cur

def crear_tablas_y_usuarios():
    # Tabla usuarios
    ejecutar("""CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        rol TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )""")
    ejecutar("""INSERT OR REPLACE INTO usuarios (nombre, rol, username, password) VALUES
        ('Dr. Juan', 'Doctor', 'docjuan', '1234'),
        ('Contador', 'Contador', 'contador', '5678'),
        ('Proveedor', 'Proveedor', 'proveedor', '9012')""")

    # Tabla productos
    ejecutar("""CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )""")

    # Tabla movimientos
    ejecutar("""CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY(producto_id) REFERENCES productos(id),
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )""")

    # Tabla fichas medicas
    ejecutar("""CREATE TABLE IF NOT EXISTS fichas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente TEXT NOT NULL,
        datos TEXT NOT NULL,
        creado_por INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY(creado_por) REFERENCES usuarios(id)
    )""")

    # Tabla citas
    ejecutar("""CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        paciente TEXT NOT NULL,
        creado_por INTEGER NOT NULL,
        registrado_en TEXT NOT NULL,
        FOREIGN KEY(creado_por) REFERENCES usuarios(id)
    )""")


# Funciones de negocio

def validar_usuario(username, password):
    cur = ejecutar("SELECT id, rol, nombre FROM usuarios WHERE username=? AND password=?", (username, password))
    return cur.fetchone()  # (id, rol, nombre) o None

def agregar_producto(nombre, precio, stock, usuario_id):
    cur = ejecutar("SELECT id, stock FROM productos WHERE nombre=?", (nombre,))
    row = cur.fetchone()
    if row:
        pid, exist = row
        ejecutar("UPDATE productos SET stock=?, precio=? WHERE id=?", (exist+stock, precio, pid))
        pid = pid
    else:
        cur = ejecutar("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))
        pid = cur.lastrowid
    ejecutar("INSERT INTO movimientos (tipo, producto_id, cantidad, usuario_id, fecha) VALUES (?, ?, ?, ?, ?)",
             ("entrada", pid, stock, usuario_id, datetime.now().isoformat()))

def vender_producto(nombre, cantidad, usuario_id):
    cur = ejecutar("SELECT id, stock FROM productos WHERE nombre=?", (nombre,))
    row = cur.fetchone()
    if not row:
        raise ValueError("Producto no existe")
    pid, stock = row
    if stock < cantidad:
        raise ValueError(f"Stock insuficiente ({stock} disponible)")
    ejecutar("UPDATE productos SET stock=? WHERE id=?", (stock-cantidad, pid))
    ejecutar("INSERT INTO movimientos (tipo, producto_id, cantidad, usuario_id, fecha) VALUES (?, ?, ?, ?, ?)",
             ("salida", pid, cantidad, usuario_id, datetime.now().isoformat()))

def obtener_productos():
    cur = ejecutar("SELECT * FROM productos")
    return cur.fetchall()

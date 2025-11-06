import os
import sqlite3
from datetime import datetime

DB_NAME = "clinica.db"

class BaseDatos:
    def __init__(self, db_file=DB_NAME):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            print(f"Base de datos {self.db_file} no existe, se creará ahora.")
        self._crear_tablas()

    def _conn(self):
        conexcion = sqlite3.connect(self.db_file, timeout=10)
        conexcion.execute("PRAGMA foreign_keys = ON")
        conexcion.row_factory = sqlite3.Row
        return conexcion

    def ejecutar(self, query, params=(), fetch=False):
        with self._conn() as conexion2:
            ejecutarcr = conexion2.cursor()
            ejecutarcr.execute(query, params)
            conexion2.commit()
            if fetch:
                return ejecutarcr.fetchall()
            if query.strip().upper().startswith("INSERT"):
                return ejecutarcr.lastrowid
            return ejecutarcr.rowcount

    def _crear_tablas(self):
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                rol TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        self.ejecutar("""
            INSERT OR IGNORE INTO usuarios (id, nombre, rol, username, password) VALUES
                (1, 'Dr. Maggie', 'Doctor', 'docanles', '1234'),
                (2, 'Contador', 'Contador', 'contalover', '5678'),
                (3, 'Proveedor', 'Proveedor', 'sifio', '9012')
        """)
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        """)
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                precio_unitario REAL,
                total REAL,
                proveedor_nombre TEXT, 
                FOREIGN KEY(producto_id) REFERENCES productos(id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        """)
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS pacientes (
                DPI INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT
            )
        """)
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS fichas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                datos TEXT NOT NULL,
                fecha TEXT NOT NULL,
                procedencia TEXT,
                ocupacion TEXT,
                antecedentes TEXT,
                fecha_nacimiento TEXT,
                FOREIGN KEY(paciente_id) REFERENCES pacientes(DPI)
            )
        """)
        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                paciente_id INTEGER NOT NULL,
                creado_por INTEGER NOT NULL,
                registrado_en TEXT NOT NULL,
                FOREIGN KEY(paciente_id) REFERENCES pacientes(DPI),
                FOREIGN KEY(creado_por) REFERENCES usuarios(id)
            )
        """)

class Usuario:
    def __init__(self, nombre, rol, db: BaseDatos):
        self.nombre = nombre
        self.rol = rol
        self.db = db
        self.id = None

    def iniciar_sesion(self, username, password):
        filas = self.db.ejecutar(
            "SELECT * FROM usuarios WHERE username=? AND password=?",
            (username, password), fetch=True
        )
        if filas:
            usuario = filas[0]
            self.id = usuario["id"]
            self.nombre = usuario["nombre"]
            self.rol = usuario["rol"]
            return usuario
        return None

class Paciente:
    def __init__(self, DPI, nombre, telefonos=None, db: BaseDatos=None):
        self.DPI = DPI
        self.nombre = nombre
        self.telefono = telefonos
        self.db = db

    def guardar(self):
        if not self.db:
            raise RuntimeError("No se proporcionó instancia de BaseDatos en Paciente")
        query = "INSERT INTO pacientes (DPI, nombre, telefono) VALUES (?, ?, ?)"
        return self.db.ejecutar(query, (self.DPI, self.nombre, self.telefono))

    @staticmethod
    def listar(db: BaseDatos):
        filas = db.ejecutar("SELECT * FROM pacientes ORDER BY DPI DESC", fetch=True)
        return filas or []

class Doctor(Usuario):
    def crear_ficha_medica(self, paciente_id, datos, procedencia=None, ocupacion=None, antecedentes=None, fecha_nacimiento=None):
        if not self.id:
            raise RuntimeError("Doctor.id no está seteado")
        self.db.ejecutar(
            """
            INSERT INTO fichas (paciente_id, datos, fecha, procedencia, ocupacion, antecedentes, fecha_nacimiento)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (paciente_id, datos, datetime.now().isoformat(), procedencia, ocupacion, antecedentes, fecha_nacimiento)
        )

class Contador(Usuario):
    def ver_inventario(self):
        productos = self.db.ejecutar("SELECT * FROM productos", fetch=True)
        return productos or []

class Proveedor(Usuario):
    def agregar_producto(self, nombre, precio, stock):
        agregarpd = self.db.ejecutar("SELECT id, stock FROM productos WHERE nombre=?", (nombre,), fetch=True)
        if agregarpd:
            PRD, exist = agregarpd[0]['id'], agregarpd[0]['stock']
            self.db.ejecutar("UPDATE productos SET stock=?, precio=? WHERE id=?", (exist+stock, precio, PRD))
        else:
            self.db.ejecutar("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))

    @staticmethod
    def vender_producto(db: BaseDatos, nombre, cantidad, doctor_user, doctor_pass, proveedor_id):
        productos = db.ejecutar("SELECT id, stock, precio FROM productos WHERE nombre=?", (nombre,), fetch=True)
        if not productos:
            raise ValueError("Producto no existe")
        pid, stock, precio_unitario = productos[0]['id'], productos[0]['stock'], productos[0]['precio']
        if stock < cantidad:
            raise ValueError(f"Stock insuficiente ({stock} disponible)")
        doctor = db.ejecutar("SELECT * FROM usuarios WHERE username=? AND password=? AND rol='Doctor'", (doctor_user, doctor_pass), fetch=True)
        if not doctor:
            raise ValueError("Autorización del doctor fallida")
        total = cantidad * precio_unitario
        db.ejecutar("UPDATE productos SET stock=? WHERE id=?", (stock-cantidad, pid))
        db.ejecutar(
            "INSERT INTO movimientos (tipo, producto_id, cantidad, usuario_id, fecha, precio_unitario, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("salida", pid, cantidad, proveedor_id, datetime.now().isoformat(), precio_unitario, total)
        )
        return {"producto": nombre, "cantidad": cantidad, "precio_unitario": precio_unitario, "total": total}

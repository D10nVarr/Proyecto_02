import os
import sqlite3

DB_FILE = "clinica.db"

def conn():
    c = sqlite3.connect(DB_FILE, timeout=10)
    c.execute("PRAGMA foreign_keys = ON")
    return c

def ejecutar(sql, params=()):
    with conn() as c:
        cur = c.cursor()
        cur.execute(sql, params)
        c.commit()
        return cur

def ejecutar_many(sql, seq_params):
    with conn() as c:
        cur = c.cursor()
        cur.executemany(sql, seq_params)
        c.commit()
        return cur

def crear_tablas():
    ejecutar("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        rol TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    ejecutar("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)
    ejecutar("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        producto_id INTEGER NOT NULL,
        cantidad INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY(producto_id) REFERENCES productos(id),
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    """)
    ejecutar("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        telefono TEXT,
        procedencia TEXT,
        ocupacion TEXT,
        antecedentes TEXT,
        fecha_nacimiento TEXT
    )
    """)
    ejecutar("""
    CREATE TABLE IF NOT EXISTS fichas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        datos TEXT NOT NULL,
        creado_por INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id),
        FOREIGN KEY(creado_por) REFERENCES usuarios(id)
    )
    """)
    ejecutar("""
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT NOT NULL,
        paciente_id INTEGER NOT NULL,
        creado_por INTEGER NOT NULL,
        registrado_en TEXT NOT NULL,
        FOREIGN KEY(paciente_id) REFERENCES pacientes(id),
        FOREIGN KEY(creado_por) REFERENCES usuarios(id)
    )
    """)

def insertar_datos_iniciales():
    ejecutar("""
    INSERT OR IGNORE INTO usuarios (id, nombre, rol, username, password) VALUES
        (1, 'Dr. Maggie', 'Doctor', 'docanles', '1234'),
        (2, 'Contador', 'Contador', 'contalover', '5678'),
        (3, 'Proveedor', 'Proveedor', 'sifio', '9012')
    """)

def main():
    crear_tablas()
    insertar_datos_iniciales()
    print("Base de datos creada en:", os.path.abspath(DB_FILE))

if __name__ == "__main__":
    main()

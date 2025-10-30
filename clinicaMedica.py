import sqlite3
from datetime import datetime

DB_NAME = "clinica.db"

class BaseDatos:
    def __init__(self, db_file=DB_NAME):
        self.db_file = db_file
        self._crear_tablas()

    def _conn(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def ejecutar(self, query, params=(), fetch=False):
        with self._conn() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            if fetch:
                return cur.fetchall()
            return cur

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
            INSERT OR IGNORE INTO usuarios (nombre, rol, username, password) VALUES
                ('Dr. Maggie', 'Doctor', 'docanles', '1234'),
                ('Contador', 'Contador', 'contalover', '5678'),
                ('Proveedor', 'Proveedor', 'sifio', '9012')
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
                FOREIGN KEY(producto_id) REFERENCES productos(id),
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
        """)

        self.ejecutar("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT,
                procedencia TEXT,
                ocupacion TEXT,
                antecendentes TEXT,
                fecha_nacimiento TEXT
            )
        """)

        self.ejecutar("""
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

        self.ejecutar("""
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


class Usuario:
    def __init__(self, nombre, rol, db: BaseDatos):
        self.nombre = nombre
        self.rol = rol
        self.db = db
        self.id=None

    def iniciar_sesion(self, username, password):
        usuario = self.db.ejecutar(
            "SELECT * FROM usuarios WHERE username=? AND password=?",
            (username, password), fetch=True
        )
        if usuario:
            print(f"{usuario[0]['nombre']} ha iniciado sesión como {usuario[0]['rol']}.")
            return usuario[0]
        print("Usuario o contraseña incorrectos")
        return None

class Paciente:
    def __init__(self, nombre, telefono, procedencia, antecedentes, fecha_nacimiento, db: BaseDatos):
        self.nombre = nombre
        self.telefono = telefono
        self.procedencia = procedencia
        self.antecedentes = antecedentes
        self.fecha_nacimiento = fecha_nacimiento
        self.db = db

    def guardar(self):
        self.db.ejecutar(
            "INSERT INTO pacientes (nombre, telefono, procedencia, ocupacion, antecedentes, fecha_nacimiento) VALUES (?, ?, ?, ?, ?, ?)",
            (self.nombre, self.telefono, self.procedencia, self.antecedentes, self.fecha_nacimiento)
        )
        print(f"Paciente '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar(db: BaseDatos):
        filas = db.ejecutar("SELECT * FROM pacientes", fetch=True)
        if not filas:
            print("No hay pacientes registrados.")
            return
        print("\n--- LISTADO DE PACIENTES ---")
        for f in filas:
            print(f"ID: {f['id']} | Nombre: {f['nombre']} | Tel: {f['telefono']} | Correo: {f['correo']} | Fecha Nac.: {f['fecha_nacimiento']}")

class Doctor(Usuario):
    def crear_ficha_medica(self, paciente_id, datos):
        self.db.ejecutar(
            "INSERT INTO fichas (paciente_id, datos, creado_por, fecha) VALUES (?, ?, ?, ?)",
            (paciente_id, datos, self.id, datetime.now().isoformat())
        )

class Contador(Usuario):
    def ver_inventario(self):
        productos = self.db.ejecutar("SELECT * FROM productos", fetch=True)
        for p in productos:
            print(f"{p['nombre']} - Stock: {p['stock']} - Precio: {p['precio']}")


class Proveedor(Usuario):
    def agregar_producto(self, nombre, precio, stock):
        cur = self.db.ejecutar("SELECT id, stock FROM productos WHERE nombre=?", (nombre,), fetch=True)
        if cur:
            pid, exist = cur[0]['id'], cur[0]['stock']
            self.db.ejecutar("UPDATE productos SET stock=?, precio=? WHERE id=?", (exist+stock, precio, pid))
        else:
            self.db.ejecutar("INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)", (nombre, precio, stock))

    def vender_producto(db: BaseDatos, nombre, cantidad, usuario_id):
        cur = db.ejecutar("SELECT id, stock FROM productos WHERE nombre=?", (nombre,), fetch=True)
        if not cur:
            raise ValueError("Producto no existe")
        pid, stock = cur[0]['id'], cur[0]['stock']
        if stock < cantidad:
            raise ValueError(f"Stock insuficiente ({stock} disponible)")
        db.ejecutar("UPDATE productos SET stock=? WHERE id=?", (stock-cantidad, pid))
        db.ejecutar(
            "INSERT INTO movimientos (tipo, producto_id, cantidad, usuario_id, fecha) VALUES (?, ?, ?, ?, ?)",
            ("salida", pid, cantidad, usuario_id, datetime.now().isoformat())
        )

#####Funcionamiento DB---------------------------------------------------------------
DatBas=BaseDatos()

print("Menu")
print("1. Iniciar sesión")

opcion=input("Seleccione una opcion: ")

match opcion:
    case "1":
        usuario=input("Ingrese su usuario: ")
        contra=input("Ingrese su contra: ")

        persona=Usuario(None,None,DatBas)

        persona.iniciar_sesion(usuario, contra)
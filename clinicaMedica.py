import sqlite3

DB_NAME = "clinica_pacientes.db"

class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def iniciar_sesion(self):
        print(f"{self.nombre} ha iniciado sesión con el rol de {self.rol}.")


class Paciente(Usuario):
    def __init__(self, nombre, telefono, correo, fecha_nacimiento):
        super().__init__(nombre, "Paciente")
        self.telefono = telefono
        self.correo = correo
        self.fecha_nacimiento = fecha_nacimiento


class Doctor(Usuario):
    def __init__(self, nombre, especialidad):
        super().__init__(nombre, "Doctor")
        self.especialidad = especialidad

    @staticmethod
    def _conn():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clinica (
                id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                carrera TEXT NOT NULL,
                promedio REAL
            );
        """)
        conn.commit()
        return conn

    def guardar(self):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO clinica (nombre, carrera, promedio) VALUES (?, ?, ?)",
                (self.nombre, self.carrera, self.promedio)
            )
        print(f"Estudiante '{self.nombre}' guardado con éxito.")

    @staticmethod
    def listar():
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM clinica")
            filas = cur.fetchall()
            if not filas:
                print("No hay estudiantes registrados.")
                return
            print("\n--- LISTADO DE ESTUDIANTES ---")
            for f in filas:
                print(f"ID: {f['id_estudiante']} | Nombre: {f['nombre']} | Carrera: {f['carrera']} | Promedio: {f['promedio']}")

    @staticmethod
    def modificar():
        ide = input("Ingrese ID del estudiante a modificar: ")
        with Estudiante._conn() as conn:
            cur = conn.execute("SELECT * FROM clinica WHERE id_estudiante = ?", (ide,))
            fila = cur.fetchone()
            if not fila:
                print("No se encontró el estudiante.")
                return
            nombre = input(f"Nuevo nombre [{fila['nombre']}]: ") or fila['nombre']
            carrera = input(f"Nueva carrera [{fila['carrera']}]: ") or fila['carrera']
            promedio = input(f"Nuevo promedio [{fila['promedio']}]: ") or fila['promedio']
            conn.execute("UPDATE estudiantes SET nombre=?, carrera=?, promedio=? WHERE id_estudiante=?",
                         (nombre, carrera, promedio, ide))
        print("Estudiante actualizado con éxito.")

    @staticmethod
    def eliminar():
        ide = input("Ingrese ID del estudiante a eliminar: ")
        with Estudiante._conn() as conn:
            cur = conn.execute("DELETE FROM clinica WHERE id_estudiante = ?", (ide,))
            if cur.rowcount == 0:
                print("No se encontró el estudiante.")
            else:
                print("Estudiante eliminado con éxito.")

    def ficha_medica(self):
        pass

    def crear_historial_medico(self):
        pass

    def crear_registro_cita(self):
        pass

    def crear_inventario(self):
        pass

    def vender_medicamento(self):
        pass

class Contador(Usuario):
    def __init__(self, nombre):
        super().__init__(nombre, "Contador")

    def ver_inventario(self):
        pass

    def agregar_medicamento(self):
        pass

class Proveedor(Usuario):
    def __init__(self, nombre):
        super().__init__(nombre, "Proveedor")

    def agregar_medicamento(self):
        pass
import customtkinter as ctk
from collections import deque
from datetime import datetime

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class Inventario:
    def __init__(self):
        self._items = {}
        self._registro = deque()

    def agregar(self, nombre, cantidad, usuario):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        prev = self._items.get(nombre, 0)
        self._items[nombre] = prev + cantidad
        self._registro.appendleft({
            "tipo": "entrada",
            "medicamento": nombre,
            "cantidad": cantidad,
            "usuario": usuario,
            "fecha": datetime.now()
        })

    def vender(self, nombre, cantidad, usuario):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que 0")
        exist = self._items.get(nombre, 0)
        if exist < cantidad:
            raise ValueError(f"Stock insuficiente para '{nombre}' (hay {exist})")
        self._items[nombre] = exist - cantidad
        if self._items[nombre] == 0:
            del self._items[nombre]
        self._registro.appendleft({
            "tipo": "salida",
            "medicamento": nombre,
            "cantidad": cantidad,
            "usuario": usuario,
            "fecha": datetime.now()
        })

    def listar(self):
        return dict(self._items)

    def registro(self, limit=100):
        return list(self._registro)[:limit]

class Usuario:
    def __init__(self, nombre, rol, app=None):
        self.nombre = nombre
        self.rol = rol
        self.app = app

    def iniciar_sesion(self):
        print(f"{self.nombre} ha iniciado sesión con el rol de {self.rol}.")

class Doctor(Usuario):
    def __init__(self, nombre, especialidad, app=None):
        super().__init__(nombre, "Doctor", app)
        self.especialidad = especialidad

    def ficha_medica(self, paciente_nombre, datos):
        self.app.guardar_ficha(paciente_nombre, datos, self.nombre)

    def crear_historial_medico(self, paciente_nombre, historial):
        self.app.guardar_historial(paciente_nombre, historial, self.nombre)

    def crear_registro_cita(self, paciente_nombre, fecha_hora, motivo):
        self.app.guardar_cita(paciente_nombre, fecha_hora, motivo, self.nombre)

    def crear_inventario(self, nombre_medicamento, cantidad):
        self.app.inventario.agregar(nombre_medicamento, cantidad, self.nombre)

    def vender_medicamento(self, nombre_medicamento, cantidad):
        self.app.inventario.vender(nombre_medicamento, cantidad, self.nombre)

class Contador(Usuario):
    def __init__(self, nombre, app=None):
        super().__init__(nombre, "Contador", app)

    def ver_inventario(self):
        return self.app.inventario.listar()

    def ver_registro(self):
        return self.app.inventario.registro()

class Proveedor(Usuario):
    def __init__(self, nombre, app=None):
        super().__init__(nombre, "Proveedor", app)

    def vender_medicamento(self, nombre_medicamento, cantidad):
        self.app.inventario.vender(nombre_medicamento, cantidad, self.nombre)




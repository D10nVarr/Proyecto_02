class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

    def iniciar_sesion(self):
        print(f"{self.nombre} ha iniciado sesión con el rol de {self.rol}.")


class Doctor(Usuario):
    def __init__(self, nombre, especialidad):
        super().__init__(nombre, "Doctor")
        self.especialidad = especialidad

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
"""
Módulo de registro de clientes y solicitudes de necesidades (versión orientada a objetos).
HU: Registro de cliente y solicitud de servicio/producto.
"""
from typing import List, Dict

NECESIDADES = {
    "1": "Asesoría técnica",
    "2": "Consulta veterinaria",
    "3": "Disponibilidad del producto",
}

class Cliente:
    def __init__(self, nombre: str, cedula: str, direccion: str, telefono: str):
        self.nombre = nombre
        self.cedula = cedula
        self.direccion = direccion
        self.telefono = telefono

    def to_dict(self) -> Dict:
        return {
            "nombre": self.nombre,
            "id": self.cedula,
            "direccion": self.direccion,
            "telefono": self.telefono,
        }

class SolicitudServicio:
    def __init__(self, cliente: Cliente, necesidad: str, cantidad: int):
        self.cliente = cliente
        self.necesidad = necesidad
        self.cantidad = cantidad

    def resumen(self) -> str:
        return (
            f"\n--- Consolidado de la solicitud ---\n"
            f"Nombre: {self.cliente.nombre}\n"
            f"Cédula: {self.cliente.cedula}\n"
            f"Dirección: {self.cliente.direccion}\n"
            f"Teléfono: {self.cliente.telefono}\n"
            f"Necesidad: {self.necesidad}\n"
            f"Cantidad: {self.cantidad}\n"
        )

class GestorSolicitudes:
    def __init__(self):
        self.clientes: List[Cliente] = []
        self.solicitudes: List[SolicitudServicio] = []
        self.citas_disponibles = 20
        self.asesorias_disponibles = 20

    # ---------------- Utilidades -----------------
    @staticmethod
    def _solicitar_numero(mensaje: str) -> str:
        while True:
            dato = input(mensaje)
            if dato.isdigit() and len(dato) == 10:
                return dato
            print("Error: Debe ingresar solo números y que tenga 10 dígitos.")

    # ---------------- Registro de Cliente ----------------
    def registrar_cliente(self) -> Cliente:
        print("\n--- Registro de clientes ---")
        while True:
            nombre = input("Ingrese el nombre del cliente: ").strip()
            if nombre:
                break
            print("Error: El nombre no puede estar vacío.")

        cedula = self._solicitar_numero("Ingrese la ID (Cédula) del cliente (10 dígitos): ")

        while True:
            direccion = input("Ingrese la dirección del cliente: ").strip()
            if direccion:
                break
            print("Error: La dirección no puede estar vacía.")

        telefono = self._solicitar_numero("Ingrese el teléfono del cliente (10 dígitos): ")

        cliente = Cliente(nombre, cedula, direccion, telefono)
        self.clientes.append(cliente)
        print("Cliente registrado exitosamente.")
        return cliente

    # ---------------- Selección de Necesidad ----------------
    def seleccionar_necesidad(self) -> str:
        print("--- Seleccione la necesidad del cliente ---")
        for key, val in NECESIDADES.items():
            print(f"{key}. {val}")

        while True:
            opcion = input("Ingrese su opción (1-3): ").strip()
            if opcion in NECESIDADES:
                return NECESIDADES[opcion]
            print("Error: Ingrese un número válido.")

    # ---------------- Ingreso de Cantidades ----------------
    def ingresar_cantidad(self, necesidad: str) -> int:
        while True:
            cantidad_str = input(f"Ingrese la cantidad de {necesidad} que desea: ").strip()
            if not cantidad_str.isdigit():
                print("Error: Ingrese solo números.")
                continue
            cantidad = int(cantidad_str)
            if cantidad <= 0:
                print("Error: La cantidad debe ser mayor que cero.")
                continue

            # Reglas de disponibilidad
            if necesidad == "Asesoría técnica":
                if cantidad > self.asesorias_disponibles:
                    print(f"Error: No hay suficientes asesorías disponibles. Solo quedan {self.asesorias_disponibles}.")
                    continue
                self.asesorias_disponibles -= cantidad
            elif necesidad == "Consulta veterinaria":
                if cantidad > self.citas_disponibles:
                    print(f"Error: No hay suficientes citas disponibles. Solo quedan {self.citas_disponibles}.")
                    continue
                self.citas_disponibles -= cantidad
            # Para disponibilidad de producto no hay control de stock en este contexto
            return cantidad

    # ---------------- Registro de Solicitud ----------------
    def crear_solicitud(self):
        cliente = self.registrar_cliente()
        necesidad = self.seleccionar_necesidad()
        cantidad = self.ingresar_cantidad(necesidad)
        solicitud = SolicitudServicio(cliente, necesidad, cantidad)
        self.solicitudes.append(solicitud)
        print(solicitud.resumen())
        print("Solicitud de servicio registrada exitosamente.\n")

# ---------------- Ejecución en modo consola -----------------
if __name__ == "__main__":
    gestor = GestorSolicitudes()
    while True:
        print("\n==== Menú ====")
        print("1. Registrar nueva solicitud")
        print("2. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            gestor.crear_solicitud()
        elif opcion == "2":
            break
        else:
            print("Opción no válida.")



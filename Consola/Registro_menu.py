from HU.producto_registro_cliente_necesidad import *

class MenuRegistros:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            cliente = registrar_cliente()
            necesidad = seleccionar_necesidad()
            cantidad = ingresar_cantidades(necesidad)

            cliente ["necesidad"] = necesidad
            cliente ["cantidad"] = cantidad

            mostrar_consolidado(cliente)
            confirmar = input("¿Desea confirmar la solicitud? (si/no): ")

            if confirmar.lower() == "si":
                confirmar_solicitud(cliente)
                print("Registro realizado exitosamente")
            else:
                print("Solicitud de servicio cancelada.")
                return
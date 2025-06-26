from Venta import Venta

class MenuVentas:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            print("\n=== MENÚ DE VENTAS ===")
            print("1. Registrar nueva venta")
            print("2. Ver ventas registradas")
            print("0. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                Venta.registrar_venta(self.inventario)

            elif opcion == "2":
                Venta.ver_ventas()

            elif opcion == "0":
                print("Volviendo al menú principal...")
                break

            else:
                print("❌ Opción inválida. Intente nuevamente.")

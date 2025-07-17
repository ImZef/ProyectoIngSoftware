from HU.Venta import Venta

class MenuVentas:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            print("\n--- Menú de Ventas ---")
            print("1. Registrar nueva venta")
            print("2. Ver ventas registradas")
            print("3. Editar venta")
            print("4. Anular venta")
            print("5. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                Venta.registrar_venta()
            elif opcion == "2":
                Venta.ver_ventas()
            elif opcion == "3":
                Venta.editar_venta()
            elif opcion == "4":
                Venta.anular_venta()
            elif opcion == "5":
                print("Saliendo del módulo de ventas.")
                break
            else:
                print("Opción inválida.")
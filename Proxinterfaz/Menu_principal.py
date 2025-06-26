from Proxinterfaz.Inventario_menu import MenuInventario
from Proxinterfaz.Venta_menu import MenuVentas
from Proxinterfaz.Registro_menu import MenuRegistros
from Proxinterfaz.Historialclinico_menu import MenuHistorialClinico


class MenuPrincipal:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Sistema de Registro de Clientes y Necesidades")
            print("2. Menú de Ventas")
            print("3. Sistema de Historial Clínico")
            print("4. Sistema de Inventario (Productos)")
            print("0. Salir")

            opcion = input("Seleccione una opción (0-4): ")

            if opcion == "1":
                menu_registro = MenuRegistros(self.inventario)
                menu_registro.mostrar_menu()

            elif opcion == "2":
                menu_ventas = MenuVentas(self.inventario)
                menu_ventas.mostrar_menu()

            elif opcion == "3":
                menu_historialclinico = MenuHistorialClinico()
                menu_historialclinico.mostrar_menu()

            elif opcion == "4":
                menu_inventario = MenuInventario(self.inventario)
                menu_inventario.mostrar_menu()
            elif opcion == "0":
                print("Gracias por usar el Sistema Veterinario. ¡Hasta pronto!")
                break

            else:
                print("Opción inválida. Por favor intente nuevamente.")

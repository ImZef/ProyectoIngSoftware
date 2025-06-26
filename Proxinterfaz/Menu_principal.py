from Proxinterfaz.Inventario_menu import MenuInventario
from Proxinterfaz.Venta_menu import MenuVentas
from Proxinterfaz.Registro_menu import MenuRegistros
from HU.HistoriaClinica import main as historial_main

class MenuPrincipal:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Sistema de Inventario (Productos)")
            print("2. Sistema de Historial Clínico")
            print("3. Menú de Ventas")
            print("4. Sistema de Registro de Clientes y Necesidades")
            print("0. Salir")

            opcion = input("Seleccione una opción (0-4): ")

            if opcion == "1":
                menu_inventario = MenuInventario(self.inventario)
                menu_inventario.mostrar_menu()

            elif opcion == "2":
                historial_main()

            elif opcion == "3":
                menu_ventas = MenuVentas(self.inventario)
                menu_ventas.mostrar_menu()

            elif opcion == "4":
                menu_registro = MenuRegistros(self.inventario)
                menu_registro.mostrar_menu()

            elif opcion == "0":
                print("Gracias por usar el Sistema Veterinario. ¡Hasta pronto!")
                break

            else:
                print("Opción inválida. Por favor intente nuevamente.")

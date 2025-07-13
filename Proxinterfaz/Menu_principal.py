from Proxinterfaz.Inventario_menu import MenuInventario
from Proxinterfaz.Venta_menu import MenuVentas
from Proxinterfaz.Registro_menu import MenuRegistros
from Proxinterfaz.Historialclinico_menu import MenuHistorialClinico

usuarios ={'admin': 'admin123', 'bod': 'bodeguero123', 'vet': 'veterinario123', 'auxventas': 'auxventas123'}
class MenuPrincipal:
    def __init__(self, inventario):
        self.inventario = inventario

    def cambiar_usuario(self):
        input("Presione Enter para continuar...")
        return MenuPrincipal(self.inventario).mostrar_menu()

    def mostrar_menu(self):
        while True:
            print("\n=== MENÚ DE INICIO ===")
            user = input("\nIngrese su usuario: ")
            cont = input("Ingrese su contraseña: ")        
            if user in usuarios and usuarios[user] == cont:
                print("\n======================")
                print(f"\nBienvenido {user}")
                break
            else:
                print("\n======================")
                print("\nUsuario o contraseña incorrectos.")
                opc = input("¿Desea intentar nuevamente? (s/n): ")
                if opc.lower() != 's':
                    print("\n=======================")
                    print("Saliendo del sistema...")
                    return
        while True:
            print("\n=== MENÚ PRINCIPAL ===")
            print("1. Sistema de Registro de Clientes y Necesidades")
            print("2. Menú de Ventas")
            print("3. Sistema de Historial Clínico")
            print("4. Sistema de Inventario (Productos)")
            print("5. Cambiar Usuario")
            print("0. Salir")

            opcion = input("Seleccione una opción (0-4): ")

            if opcion == "1":
                if user in ['admin', 'auxventas']:
                    menu_registro = MenuRegistros(self.inventario)
                    menu_registro.mostrar_menu()
                else:
                    print("Acceso denegado. Solo el administrador o auxiliar de ventas pueden acceder al sistema de registro.")

            elif opcion == "2":
                if user in ['admin', 'auxventas']:
                    menu_ventas = MenuVentas(self.inventario)
                    menu_ventas.mostrar_menu()
                else:
                    print("Acceso denegado. Solo el administrador o auxiliar de ventas pueden acceder al menú de ventas.")
            
            elif opcion == "3":
                if user == 'vet':
                    menu_historialclinico = MenuHistorialClinico()
                    menu_historialclinico.mostrar_menu()
                else:
                    print("Acceso denegado. Solo el veterinario puede acceder a los historiales clínicos.")

            elif opcion == "4":
                if user in ['admin', 'bod', 'auxventas']:
                    menu_inventario = MenuInventario(self.inventario)
                    menu_inventario.mostrar_menu()
                else:
                    print("Acceso denegado. Solo el administrador, bodeguero o auxiliar de ventas pueden acceder al inventario.")
            
            elif opcion == "5":
                print("\nCerrando sesión...")
                return self.cambiar_usuario()
                
            elif opcion == "0":
                print("Gracias por usar el Sistema Veterinario. ¡Hasta pronto!")
                break
            
            else:
                print("Opción inválida. Por favor intente nuevamente.")
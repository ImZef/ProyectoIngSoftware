from Inventario import Inventario

class MenuInventario:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            print("\n--- Menú de Inventario ---")
            print("1. Listar productos")
            print("2. Actualizar stock")
            print("3. Ver historial de cambios de stock")
            print("0. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.inventario.listar_productos()
            elif opcion == "2":
                self.actualizar_stock()
            elif opcion == "3":
                self.inventario.mostrar_historial()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")

    def actualizar_stock(self):
        identificador = input("ID o nombre del producto: ")
        try:
            nueva_cantidad = int(input("Nueva cantidad: "))
            motivo = input("Motivo del ajuste: ")
            self.inventario.actualizar_stock(identificador, nueva_cantidad, motivo)
        except ValueError:
            print("Cantidad inválida.")

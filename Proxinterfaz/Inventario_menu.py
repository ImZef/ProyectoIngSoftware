from HU.Inventario import Inventario
from HU.Producto import Producto

class MenuInventario:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Inventario ---")
            print("1. Consultar producto ")
            print("2. Ver todos los productos")
            print("3. Actualizar stock")
            print("4. Ver historial de stock")
            print("0. Volver")

            opcion = input("Elige opción: ")

            if opcion == "1":
                self.consultar_producto()
            elif opcion == "2":
                self.inventario.listar_productos()
            elif opcion == "3":
                cod = input("Código: ")
                nueva_cant = int(input("Nueva cantidad: "))
                motivo = input("Motivo: ")
                self.inventario.actualizar_stock(cod, nueva_cant, motivo)
            elif opcion == "4":
                self.inventario.mostrar_historial()
            elif opcion == "0":
                break
            else:
                print("Opción inválida.")

    # === CONSULTAR PRODUCTO CON TODOS LOS CASOS DE LA HU06 ===
    def consultar_producto(self):
        print("\n=== CONSULTAR PRODUCTO ===")
        modo_busqueda = input("Buscar por (1) Código, (2) Nombre, (3) Categoría: ")

        producto = None
        if modo_busqueda == "1":
            codigo = input("Ingrese código del producto: ")
            producto = self.inventario.buscar_por_codigo(codigo)
        elif modo_busqueda == "2":
            nombre = input("Ingrese nombre del producto: ")
            producto = self.inventario.buscar_por_nombre(nombre)
        elif modo_busqueda == "3":
            categoria = input("Ingrese categoría: ")
            productos = self.inventario.buscar_por_categoria(categoria)
            if productos:
                print("\nProductos encontrados en categoría:")
                for p in productos:
                    print(p)
            else:
                print("No hay productos registrados en esa categoría.")
            return
        else:
            print("Opción no válida.")
            return

        # Verificar resultado de búsqueda
        if producto:
            print("\n Producto encontrado:")
            print(producto)

            if producto.get_cantidad() > 0:
                print(" Producto disponible para venta.")
            else:
                print(" Producto AGOTADO.")
                respuesta = input("¿Desea programar reposición? (s/n): ").lower()
                if respuesta == 's':
                    try:
                        nueva_cant = int(input("Ingrese cantidad a reponer: "))
                        motivo = input("Motivo de reposición: ")
                        self.inventario.actualizar_stock(producto.get_codigo(), nueva_cant, motivo)
                    except ValueError:
                        print(" Error: la cantidad debe ser numérica.")
        else:
            print(" Producto NO registrado en el sistema.")
            respuesta = input("¿Desea registrarlo ahora? (s/n): ").lower()
            if respuesta == 's':
                try:
                    nuevo_codigo = int(input("Código: "))
                    nuevo_nombre = input("Nombre: ")
                    nueva_categoria = input("Categoría: ")
                    nueva_desc = input("Descripción: ")
                    nuevo_precio = float(input("Precio: "))
                    nueva_cantidad = int(input("Cantidad inicial: "))
                    nueva_fecha = input("Fecha de vencimiento (dd/mm/aaaa o N/A): ")

                    nuevo_producto = Producto(nuevo_codigo, nuevo_nombre, nueva_categoria,
                                              nueva_desc, nuevo_precio, nueva_cantidad, nueva_fecha)
                    self.inventario.agregar_producto(nuevo_producto)
                    self.inventario.guardar_en_json()
                    print(" Producto registrado correctamente.")
                except Exception as e:
                    print(f" Error al registrar producto: {e}")

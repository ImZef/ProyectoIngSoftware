from HU.Inventario import Inventario
from HU.Producto import Producto

class MenuInventario:
    def __init__(self, inventario):
        self.inventario = inventario

    def mostrar_menu(self):
        while True:
            print("\n--- Menú Inventario ---")
            print("1. Consultar producto (HU06)")
            print("2. Ver todos los productos")
            print("3. Actualizar stock")
            print("4. Ver historial de stock")
            print("5. Crear nuevo producto")
            print("6. Ver productos próximos a agotarse")
            print("7. Cambiar umbral de stock bajo")
            print("0. Volver")
            
            cant, prod = self.inventario.listar_productos_bajos(ptr=False)
            if cant > 0:
                print("---------------------------")
                print(f"⚠️  Hay {cant} productos que requieren atención")
                print("---------------------------")
            
            opcion = input("Elige opción: ")

            if opcion == "1":
                self.mostrar_consulta_producto()
            elif opcion == "2":
                self.inventario.listar_productos()
            elif opcion == "3":
                self.actualizar_stock()
            elif opcion == "4":
                self.inventario.mostrar_historial()
            elif opcion == "5":
                self.crear_nuevo_producto()
            elif opcion == "6":
                self.inventario.listar_productos_bajos()
            elif opcion == "7":
                nuevo_umbral = input("Ingrese el nuevo umbral de stock bajo: ")
                self.inventario.cambiar_umbral_stock_bajo(nuevo_umbral)
            elif opcion == "0":
                break
            else:
                print(" Opción inválida.")

    def actualizar_stock(self):
        print("\n=== ACTUALIZAR STOCK ===")

        producto = self.consultar_producto()
        if not producto:
            return

        try:
            nueva_cant = int(input("Nueva cantidad: "))
            if nueva_cant < 0:
                print(" La cantidad no puede ser negativa.")
                return
        except ValueError:
            print(" Error: La cantidad debe ser un número entero.")
            return

        motivo = input("Motivo de actualización: ").strip()
        if not motivo:
            print(" Motivo requerido.")
            return

        self.inventario.actualizar_stock(producto.get_codigo(), nueva_cant, motivo)

        if nueva_cant < 5:
            print(" ADVERTENCIA: Producto próximo a agotarse (menos de 5 unidades disponibles).")

    def consultar_producto(self):
        print("\n=== BUSCAR PRODUCTO ===")
        modo_busqueda = input("Buscar por (1) Código, (2) Nombre, (3) Categoría: ").strip()

        producto = None
        if modo_busqueda == "1":
            codigo = input("Código: ")
            if codigo.isdigit():
                producto = self.inventario.buscar_por_codigo(codigo)
            else:
                print(" El código debe ser numérico.")
                return None

        elif modo_busqueda == "2":
            nombre = input("Nombre del producto: ").strip()
            producto = self.inventario.buscar_por_nombre(nombre)

        elif modo_busqueda == "3":
            categoria = input("Categoría del producto: ").strip()
            productos = self.inventario.buscar_por_categoria(categoria)
            if productos:
                print("\nProductos encontrados en esa categoría:")
                for p in productos:
                    print(p)
            else:
                print(" No se encontraron productos en esa categoría.")
            return None

        else:
            print(" Opción inválida.")
            return None

        if producto:
            print("\n Producto encontrado:")
            print(producto)
        else:
            print(" Producto no encontrado.")

        return producto

    def mostrar_consulta_producto(self):
        producto = self.consultar_producto()
        if not producto:
            respuesta = input("¿Desea registrarlo ahora? (s/n): ").lower()
            if respuesta == 's':
                self.crear_nuevo_producto()

    def crear_nuevo_producto(self):
        print("\n=== CREAR NUEVO PRODUCTO ===")
        try:
            codigo = int(input("Código: "))
            if self.inventario.buscar_por_codigo(codigo):
                print(" Ya existe un producto con ese código.")
                return

            nombre = input("Nombre: ").strip()
            if self.inventario.buscar_por_nombre(nombre):
                print(" Ya existe un producto con ese nombre.")
                return

            categoria = input("Categoría: ")
            descripcion = input("Descripción: ")
            precio = float(input("Precio: "))
            cantidad = int(input("Cantidad inicial: "))
            fecha_vencimiento = input("Fecha de vencimiento (dd/mm/aaaa o N/A): ")

            nuevo_producto = Producto(codigo, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento)
            self.inventario.agregar_producto(nuevo_producto)
            self.inventario.guardar_en_json()
            print(" Producto creado y guardado exitosamente.")

        except ValueError:
            print(" Error: Datos numéricos inválidos.")
        except Exception as e:
            print(f" Error al crear producto: {e}")

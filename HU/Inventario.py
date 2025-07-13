import json
from datetime import datetime
from .Producto import Producto


class Inventario:
    def __init__(self):
        self.productos = []
        self.umbral_stock_bajo = 5  # Definir el umbral de stock bajo

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def listar_productos(self):
        print("\n--- Listado de productos ---")
        for producto in self.productos:
            print(producto)
            if producto.get_cantidad() < 5:
                print("⚠️  Producto próximo a agotarse (stock bajo)\n")

    def listar_productos_bajos(self, ptr = True):
        if ptr:
            print("\n---⚠️ Productos próximos a agotarse (stock bajo) ---")
        productos_bajos = 0 #variable que rertorna la cantidad de productos con stock bajo
        prods = []
        for producto in self.productos:
            if producto.get_cantidad() < self.umbral_stock_bajo:
                productos_bajos += 1
                prods.append(producto.nombre)
                if ptr:
                    print(f'Código: {producto.codigo} Producto: {producto.nombre} Cantidad: {producto.cantidad}')
        if productos_bajos == 0 and ptr:
            print("No hay productos con stock bajo.")
        return (productos_bajos, prods)
    
    def cambiar_umbral_stock_bajo(self, nuevo_umbral):  # Esta funcion solo puede ser usada por el admnistrador o bodeguero
        try:
            nuevo_umbral = int(nuevo_umbral)
            if nuevo_umbral < 0:
                print("El umbral no puede ser negativo.")
                return
            self.umbral_stock_bajo = nuevo_umbral
            print(f"Umbral de stock bajo actualizado a {self.umbral_stock_bajo}.")
        except ValueError:
            print("Error: El umbral debe ser un número entero.")
        
    def buscar_por_codigo(self, codigo):
        for p in self.productos:
            if p.get_codigo() == int(codigo):
                return p
        return None

    def buscar_por_nombre(self, nombre):
        for p in self.productos:
            if p.get_nombre().lower() == nombre.lower():
                return p
        return None

    def buscar_por_categoria(self, categoria):
        return [p for p in self.productos if p.get_categoria().lower() == categoria.lower()]

    def actualizar_stock(self, codigo, nueva_cantidad, motivo):
        producto = self.buscar_por_codigo(codigo)
        if producto:
            anterior = producto.get_cantidad()
            if nueva_cantidad < 0:
                print("Error: La cantidad no puede ser negativa.")
                return
            producto.set_cantidad(nueva_cantidad)
            self.registrar_historial(producto, anterior, nueva_cantidad, motivo)
            self.guardar_en_json()
            print(f"Stock actualizado para '{producto.get_nombre()}' de {anterior} a {nueva_cantidad}.")
        else:
            print("Producto no encontrado.")

    def registrar_historial(self, producto, anterior, nuevo, motivo):
        registro = {
            "codigo_producto": producto.get_codigo(),
            "nombre_producto": producto.get_nombre(),
            "stock_anterior": anterior,
            "nuevo_stock": nuevo,
            "motivo": motivo,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        try:
            with open("historial_stock.json", "r") as archivo:
                historial = json.load(archivo)
        except FileNotFoundError:
            historial = []

        historial.append(registro)
        with open("historial_stock.json", "w") as archivo:
            json.dump(historial, archivo, indent=4)

    def mostrar_historial(self):
        try:
            with open("historial_stock.json", "r") as archivo:
                historial = json.load(archivo)
                for registro in historial:
                    print(f"{registro['fecha']} - {registro['nombre_producto']} - {registro['stock_anterior']} -> {registro['nuevo_stock']} | Motivo: {registro['motivo']}")
        except FileNotFoundError:
            print("No hay historial aún.")

    def guardar_en_json(self, archivo="productos.json"):
        productos_serializables = []
        for p in self.productos:
            producto_dict = {
                "codigo": p.get_codigo(),
                "nombre": p.get_nombre(),
                "categoria": p.get_categoria(),
                "descripcion": p.get_descripcion(),
                "precio": p.get_precio(),
                "cantidad": p.get_cantidad(),
                "disponibilidad": p.get_disponibilidad(),
                "fecha_vencimiento": p.get_fecha_vencimiento()
            }
            productos_serializables.append(producto_dict)

        with open(archivo, "w") as f:
            json.dump(productos_serializables, f, indent=4)
        print(f" Productos guardados en {archivo}.")

    def cargar_desde_json(self, archivo="productos.json"):
        # Limpiar lista de productos antes de recargar
        self.productos.clear()
        try:
            with open(archivo, "r") as f:
                productos_cargados = json.load(f)
                for p in productos_cargados:
                    producto = Producto(
                        p["codigo"],
                        p["nombre"],
                        p["categoria"],
                        p["descripcion"],
                        p["precio"],
                        p["cantidad"],
                        p["fecha_vencimiento"]
                    )
                    self.agregar_producto(producto)
            print(f" Productos cargados desde {archivo}.")
        except FileNotFoundError:
            print(f" Archivo {archivo} no encontrado. Se iniciará inventario vacío.")
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
            self.registrar_historial_stock(codigo, anterior, nueva_cantidad, motivo)
            self.guardar_en_json()
            print(f"Stock actualizado para '{producto.get_nombre()}' de {anterior} a {nueva_cantidad}.")
        else:
            print("Producto no encontrado.")

    def registrar_historial_stock(self, codigo, stock_anterior, nuevo_stock, motivo):
        """Registrar un cambio en el historial de stock."""
        historial = []
        try:
            with open("db/historial_stock.json", "r") as archivo:
                historial = json.load(archivo)
        except FileNotFoundError:
            historial = []

        producto = self.buscar_por_codigo(codigo)
        entrada = {
            "codigo_producto": codigo,
            "nombre_producto": producto.get_nombre() if producto else "Producto desconocido",
            "stock_anterior": stock_anterior,
            "nuevo_stock": nuevo_stock,
            "motivo": motivo,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        historial.append(entrada)
        with open("db/historial_stock.json", "w") as archivo:
            json.dump(historial, archivo, indent=4)

    def obtener_historial_stock(self):
        """Obtener el historial completo de cambios de stock."""
        try:
            with open("db/historial_stock.json", "r") as archivo:
                return json.load(archivo)
        except FileNotFoundError:
            return []

    def mostrar_historial(self):
        try:
            with open("db/historial_stock.json", "r") as archivo:
                historial = json.load(archivo)
                for registro in historial:
                    print(f"{registro['fecha']} - {registro['nombre_producto']} - {registro['stock_anterior']} -> {registro['nuevo_stock']} | Motivo: {registro['motivo']}")
        except FileNotFoundError:
            print("No hay historial aún.")

    def guardar_en_json(self, archivo="db/productos.json"):
        """Guardar la lista de productos en un archivo JSON."""
        with open(archivo, "w") as f:
            json.dump([p.to_dict() for p in self.productos], f, indent=4)
        
    def cargar_desde_json(self, archivo="db/productos.json"):
        # Limpiar lista de productos antes de recargar
        self.productos.clear()
        from pathlib import Path
        try:
            if not Path(archivo).exists():
                print(f" Archivo {archivo} no encontrado. Se iniciará inventario vacío.")
                return

            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido:
                    print(f" Archivo {archivo} vacío. Inventario vacío.")
                    return
                productos_cargados = json.loads(contenido)
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
        except (FileNotFoundError, json.JSONDecodeError):
            print(f" Archivo {archivo} dañado o vacío. Se iniciará inventario vacío.")
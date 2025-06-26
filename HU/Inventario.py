import json
from datetime import datetime
from .Producto import Producto


class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def listar_productos(self):
        print("\n--- Listado de productos ---")
        for producto in self.productos:
            print(producto)

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


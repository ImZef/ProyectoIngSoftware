import json
from datetime import datetime

class Inventario:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def buscar_producto(self, identificador):
        for producto in self.productos:
            if str(producto._codigo) == str(identificador) or producto._nombre.lower() == identificador.lower():
                return producto
        return None

    def listar_productos(self):
        print("\n Listado de productos en inventario:")
        for producto in self.productos:
            print(f"ID: {producto._codigo}, Nombre: {producto._nombre}, Stock: {producto._cantidad}")

    def actualizar_stock(self, identificador, nueva_cantidad, motivo):
        producto = self.buscar_producto(identificador)
        if producto:
            if nueva_cantidad < 0:
                print(" Error: La cantidad no puede ser negativa.")
                return False
            anterior = producto._cantidad
            producto._cantidad = nueva_cantidad
            print(f" Stock actualizado: '{producto._nombre}' de {anterior} a {nueva_cantidad}. Motivo: {motivo}")
            self.registrar_historial(producto, anterior, nueva_cantidad, motivo)
            return True
        else:
            print(" Producto no encontrado.")
            return False

    def registrar_historial(self, producto, stock_anterior, nuevo_stock, motivo):
        registro = {
            "codigo_producto": producto._codigo,
            "nombre_producto": producto._nombre,
            "stock_anterior": stock_anterior,
            "nuevo_stock": nuevo_stock,
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
                print("\n Historial de cambios de stock:")
                for registro in historial:
                    print(f"{registro['fecha']} - Producto: {registro['nombre_producto']}, Cambio: {registro['stock_anterior']} -> {registro['nuevo_stock']}, Motivo: {registro['motivo']}")
        except FileNotFoundError:
            print("No hay historial registrado aún.")

    

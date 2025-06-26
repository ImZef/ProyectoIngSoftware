class Producto:
    def __init__(self, codigo, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento):
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.disponibilidad = cantidad > 0
        self.fecha_vencimiento = fecha_vencimiento

    # Getters
    def get_codigo(self):
        return self.codigo

    def get_nombre(self):
        return self.nombre

    def get_categoria(self):
        return self.categoria

    def get_descripcion(self):
        return self.descripcion

    def get_precio(self):
        return self.precio

    def get_cantidad(self):
        return self.cantidad

    def get_disponibilidad(self):
        return self.disponibilidad

    def get_fecha_vencimiento(self):
        return self.fecha_vencimiento

    # Setters
    def set_cantidad(self, cantidad):
        self.cantidad = cantidad
        self.disponibilidad = cantidad > 0

    def __str__(self):
        return (
            f"Producto:\n"
            f"  Código: {self.codigo}\n"
            f"  Nombre: {self.nombre}\n"
            f"  Categoría: {self.categoria}\n"
            f"  Descripción: {self.descripcion}\n"
            f"  Precio: ${self.precio}\n"
            f"  Cantidad: {self.cantidad} {'[AGOTADO]' if self.cantidad == 0 else ''}\n"
            f"  Disponibilidad: {'Sí' if self.disponibilidad else 'No'}\n"
            f"  Fecha de Vencimiento: {self.fecha_vencimiento}"
        )

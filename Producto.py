class Producto:
    productos = [] # Lista de objetos de la clase Producto

    def __init__(self, codigo, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento):
        self._codigo = codigo # int
        self._nombre = nombre # string
        self._categoria = categoria # string
        self._descripcion = descripcion # string
        self._precio = precio # int
        self._cantidad = cantidad # int
        if cantidad > 0:
            self._disponibilidad = True # boolean
        else:
            self._disponibilidad = False # boolean
        self._fecha_vencimiento = fecha_vencimiento # string
        Producto.productos.append(self)

    # Métodos get_ y set_
    def get_codigo(self):
        return self._codigo

    def set_codigo(self, valor):
        self._codigo = valor

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombre):
        self._nombre = nombre

    def get_categoria(self):
        return self._categoria

    def set_categoria(self, categoria):
        self._categoria = categoria

    def get_descripcion(self):
        return self._descripcion

    def set_descripcion(self, descripcion):
        self._descripcion = descripcion

    def get_precio(self):
        return self._precio

    def set_precio(self, precio):
        if precio >= 0:
            self._precio = precio
        else:
            raise ValueError("El precio no puede ser negativo")

    def get_cantidad(self):
        return self._cantidad

    def set_cantidad(self,cantidad):
        if cantidad >= 0:
            self._cantidad = cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")

    def get_disponibilidad(self):
        return self._disponibilidad

    def set_disponibilidad(self, disponibilidad):
        self._disponibilidad = disponibilidad

    def get_fecha_vencimiento(self):
        return self._fecha_vencimiento

    def set_fecha_vencimiento(self, fecha_vencimiento):
        self._fecha_vencimiento = fecha_vencimiento
        
    def __str__(self):
        return (
            f"Producto:\n"
            f"  Código: {self.get_codigo()}\n"
            f"  Nombre: {self.get_nombre()}\n"
            f"  Categoría: {self.get_categoria()}\n"
            f"  Descripción: {self.get_descripcion()}\n"
            f"  Precio: ${self.get_precio()}\n"
            f"  Cantidad: {self.get_cantidad()} {'[AGOTADO]' if self.get_cantidad() == 0 else ''}\n"
            f"  Disponibilidad: {'Sí' if self.get_disponibilidad() else 'No'}\n"
            f"  Fecha de Vencimiento: {self.get_fecha_vencimiento()}"
        )
        
    @classmethod
    def ver_productos(cls):
        print("----------------------------------------------------------------------------------------------------------")
        print("Productos en inventario: ")
        print("----------------------------------------------------------------------------------------------------------")
        for producto in cls.productos:
            print(f"Codigo: {producto.get_codigo()} Nombre: {producto.get_nombre()} Categoria: {producto.get_categoria()}")
        return

    @classmethod
    def consultar_codigo(cls, codigo): # Metodo de clase: busca un producto segun su codigo
        for producto in cls.productos:
            if producto.get_codigo() == int(codigo):
                print(producto)
                return
        print("------------------------------------------")
        print("Codigo de producto no encontrado")
        print("------------------------------------------")
        print("Seleccione una de las siguientes opciones:")
        print("1: Ver inventario completo")
        print("2: Crear nueva entrada en el inventario")
        print("3: salir")
        print("------------------------------------------")
        opcion = int(input("escriba su opcion aqui: "))
        
        if opcion == 3:
            print("Programa terminado")
            return
        elif opcion == 2:
            # Recolección de datos del usuario
            codigo = int(input("Ingrese código: "))
            nombre = input("Ingrese nombre: ")
            categoria = input("Ingrese categoría: ")
            descripcion = input("Ingrese descripción: ")
            
            precio = int(input("Ingrese precio: "))
            if precio < 0:
                print("El precio no puede ser un numero negativo")
                precio = int(input("Ingrese precio: "))
            
            cantidad = int(input("Ingrese cantidad: "))
            if cantidad < 0:
                print("La cantidad no puede ser un numero negativo")
                cantidad = int(input("Ingrese cantidad: "))
            
            fecha_vencimiento = input("Ingrese fecha de vencimiento (dd/mm/aaaa): ")            
            prod = Producto(codigo, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento)
            print("Producto registrado con exito")
            print(prod)
            return
        elif opcion == 1:
            cls.ver_productos()
            return
        else:
            print("opcion no valida")
            return
            
    @classmethod
    def consultar_categoria(cls, categoria): # Metodo de clase: busca un producto segun su categoria
        c = False # variable de control
        for producto in cls.productos:
            if producto.get_categoria() == categoria:
                c = True # Si hay productos con la categoria deseada se pone True
                print(producto)
        if c: # Consulta sexitosa, se retorna
            return
        print("------------------------------------------")
        print("Categoria de productos no encontrada")
        print("------------------------------------------")
        print("Seleccione una de las siguientes opciones:")
        print("1: Ver inventario completo")
        print("2: Crear nueva entrada en el inventario")
        print("3: salir")
        print("------------------------------------------")
        opcion = int(input("escriba su opcion aqui: "))
        
        if opcion == 3:
            print("Programa terminado")
            return
        elif opcion == 2:
            # Recolección de datos del usuario
            codigo = int(input("Ingrese código: "))
            nombre = input("Ingrese nombre: ")
            categoria = input("Ingrese categoría: ")
            descripcion = input("Ingrese descripción: ")
            
            precio = int(input("Ingrese precio: "))
            if precio < 0:
                print("El precio no puede ser un numero negativo")
                precio = int(input("Ingrese precio: "))
            
            cantidad = int(input("Ingrese cantidad: "))
            if cantidad < 0:
                print("La cantidad no puede ser un numero negativo")
                cantidad = int(input("Ingrese cantidad: "))
            
            fecha_vencimiento = input("Ingrese fecha de vencimiento (dd/mm/aaaa): ")            
            prod = Producto(codigo, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento)
            print("Producto registrado con exito")
            print(prod)
            return
        elif opcion == 1:
            cls.ver_productos()
            return
        else:
            print("opcion no valida")
            return
            
    @classmethod
    def consultar_nombre(cls, nombre): # Metodo de clase: busca un producto segun su nombre
        for producto in cls.productos:
            if producto.get_nombre() == nombre:
                print(producto)
                return
        print("------------------------------------------")
        print("Nombre de producto no encontrado")
        print("------------------------------------------")
        print("Seleccione una de las siguientes opciones:")
        print("1: Ver inventario completo")
        print("2: Crear nueva entrada en el inventario")
        print("3: salir")
        print("------------------------------------------")
        opcion = int(input("escriba su opcion aqui: "))
        
        if opcion == 3:
            print("Programa terminado")
            return
        elif opcion == 2:
            # Recolección de datos del usuario
            codigo = int(input("Ingrese código: "))
            nombre = input("Ingrese nombre: ")
            categoria = input("Ingrese categoría: ")
            descripcion = input("Ingrese descripción: ")
            
            precio = int(input("Ingrese precio: "))
            if precio < 0:
                print("El precio no puede ser un numero negativo")
                precio = int(input("Ingrese precio: "))
            
            cantidad = int(input("Ingrese cantidad: "))
            if cantidad < 0:
                print("La cantidad no puede ser un numero negativo")
                cantidad = int(input("Ingrese cantidad: "))
            
            fecha_vencimiento = input("Ingrese fecha de vencimiento (dd/mm/aaaa): ")            
            prod = Producto(codigo, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento)
            print("Producto registrado con exito")
            print(prod)
            return
        elif opcion == 1:
            cls.ver_productos()
            return
        else:
            print("opcion no valida")
            return
        
        
def main():
    while True:
        print("\n--- Menú de Productos ---")
        print("1. Ver productos")
        print("2. Consultar producto por código")
        print("3. Consultar producto por nombre")
        print("4. Consultar productos por categoría")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            Producto.ver_productos()
        elif opcion == "2":
            codigo = input("Ingrese el código del producto: ")
            Producto.consultar_codigo(codigo)
        elif opcion == "3":
            nombre = input("Ingrese el nombre del producto: ")
            Producto.consultar_nombre(nombre)
        elif opcion == "4":
            categoria = input("Ingrese la categoría del producto: ")
            Producto.consultar_categoria(categoria)
        elif opcion == "5":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente nuevamente.")
            
if __name__ == "__main__":
    main()
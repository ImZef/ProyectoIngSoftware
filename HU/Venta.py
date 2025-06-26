from datetime import datetime
from HU.Producto import Producto

class Venta:
    ventas = []  # Lista de ventas realizadas

    def __init__(self, cliente, productos_vendidos, forma_pago, fecha_venta=None):
        self.cliente = cliente
        self.productos_vendidos = productos_vendidos  # Lista de tuplas (Producto, cantidad)
        self.forma_pago = forma_pago
        self.fecha_venta = fecha_venta or datetime.now()
        Venta.ventas.append(self)
        self.actualizar_inventario()

    def actualizar_inventario(self):
        for producto, cantidad in self.productos_vendidos:
            producto.set_cantidad(producto.get_cantidad() - cantidad)
            producto.set_disponibilidad(producto.get_cantidad() > 0)

    def total(self):
        return sum(prod.get_precio() * cant for prod, cant in self.productos_vendidos)

    def __str__(self):
        detalle = "\n".join([f"  - {prod.get_nombre()} x{cant} @ {prod.get_precio()}" 
                             for prod, cant in self.productos_vendidos])
        return (
            f"Venta a: {self.cliente}\n"
            f"Fecha: {self.fecha_venta.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Forma de pago: {self.forma_pago}\n"
            f"Productos:\n{detalle}\n"
            f"Total: ${self.total()}"
        )

    @classmethod
    def registrar_venta(cls):
        print("\n--- Registrar nueva venta ---")
        while True:
            cliente = input("Nombre del cliente: ").strip()
            if cliente:
                break
            print("El nombre del cliente no puede estar vacío.")
        while True:
            forma_pago = input("Forma de pago (efectivo, tarjeta): ").strip().lower()
            if forma_pago in ("efectivo", "tarjeta"):
                break
            print("Método de pago no válido. Usa 'efectivo' o 'tarjeta'.")
        fecha_input = input("Fecha de venta (dd/mm/aaaa) o Enter para usar fecha actual: ")
        if fecha_input.strip():
            try:
                fecha_venta = datetime.strptime(fecha_input, "%d/%m/%Y")
            except ValueError:
                print("Formato inválido. Se usará la fecha actual.")
                fecha_venta = datetime.now()
        else:
            fecha_venta = datetime.now()

        productos_vendidos = []

        while True:
            Producto.ver_productos()
            cod = input("Código del producto a vender (0 para finalizar): ")
            if cod == "0":
                break
            producto = next((p for p in Producto.productos if p.get_codigo() == int(cod)), None)
            if producto:
                cantidad = int(input(f"Ingrese cantidad para {producto.get_nombre()} (disponibles: {producto.get_cantidad()}): "))
                if 0 < cantidad <= producto.get_cantidad():
                    productos_vendidos.append((producto, cantidad))
                else:
                    print("Cantidad inválida o insuficiente.")
            else:
                print("Producto no encontrado.")

        if productos_vendidos:
            venta = Venta(cliente, productos_vendidos, forma_pago, fecha_venta)
            print("\n--- Venta registrada exitosamente ---")
            print(venta)
        else:
            print("No se registró ninguna venta.")

    @classmethod
    def ver_ventas(cls):
        if not cls.ventas:
            print("No hay ventas registradas.")
        for i, venta in enumerate(cls.ventas, 1):
            print(f"\n--- Venta #{i} ---")
            print(venta)

    @classmethod
    def editar_venta(cls):
        cls.ver_ventas()
        index = int(input("Número de venta a editar: ")) - 1
        if 0 <= index < len(cls.ventas):
            venta = cls.ventas[index]
            print("Editando venta:")
            print(venta)
            opcion = input("¿Desea editar cliente (c), productos (p) o forma de pago (f)? ")
            if opcion == 'c':
                nuevo = input("Nuevo nombre de cliente: ")
                venta.cliente = nuevo
            elif opcion == 'f':
                nuevo = input("Nueva forma de pago: ")
                venta.forma_pago = nuevo
            elif opcion == 'p':
                print("Los productos anteriores serán descartados.")
                venta.productos_vendidos = []
                venta.actualizar_inventario()  # Reversar cantidades (si se desea)
                cls.registrar_venta()
            print("Venta actualizada.")
        else:
            print("Venta no válida.")

    @classmethod
    def anular_venta(cls):
        cls.ver_ventas()
        index = int(input("Número de venta a anular: ")) - 1
        if 0 <= index < len(cls.ventas):
            venta = cls.ventas.pop(index)
            # Revertir inventario
            for producto, cantidad in venta.productos_vendidos:
                producto.set_cantidad(producto.get_cantidad() + cantidad)
                producto.set_disponibilidad(True)
            print("Venta anulada correctamente.")
        else:
            print("Venta no encontrada.")


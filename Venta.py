from datetime import datetime

class Venta:
    ventas = []  # Lista de ventas realizadas

    def __init__(self, cliente, productos_vendidos, forma_pago, fecha_venta=None):
        self.cliente = cliente
        self.productos_vendidos = productos_vendidos  # Lista de tuplas: (Producto, cantidad)
        self.forma_pago = forma_pago
        self.fecha_venta = fecha_venta or datetime.now()
        Venta.ventas.append(self)

    def total(self):
        return sum(producto._precio * cantidad for producto, cantidad in self.productos_vendidos)

    def __str__(self):
        detalle = "\n".join([
            f"  - {producto._nombre} x{cantidad} @ {producto._precio} c/u"
            for producto, cantidad in self.productos_vendidos
        ])
        return (
            f"\n Venta a: {self.cliente}\n"
            f"Fecha: {self.fecha_venta.strftime('%d/%m/%Y %H:%M:%S')}\n"
            f"Forma de pago: {self.forma_pago}\n"
            f"Productos:\n{detalle}\n"
            f"Total: ${self.total()}"
        )

    @classmethod
    def registrar_venta(cls, inventario):
        print("\n--- Registrar nueva venta ---")
        cliente = input("Nombre del cliente: ")
        forma_pago = input("Forma de pago (efectivo, tarjeta, etc.): ")

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
            inventario.listar_productos()
            cod = input("Código del producto a vender (0 para finalizar): ")
            if cod == "0":
                break

            producto = inventario.buscar_producto(cod)
            if producto:
                try:
                    cantidad = int(input(f"Ingrese cantidad para {producto._nombre} (disponibles: {producto._cantidad}): "))
                    if 0 < cantidad <= producto._cantidad:
                        productos_vendidos.append((producto, cantidad))
                        producto._cantidad -= cantidad  # Actualiza el stock
                        print(f" Se descontaron {cantidad} unidades de '{producto._nombre}'.")
                    else:
                        print(" Cantidad inválida o insuficiente.")
                except ValueError:
                    print(" La cantidad debe ser un número entero.")
            else:
                print(" Producto no encontrado.")

        if productos_vendidos:
            venta = Venta(cliente, productos_vendidos, forma_pago, fecha_venta)
            print("\n Venta registrada exitosamente:")
            print(venta)
        else:
            print("No se registró ninguna venta.")

    @classmethod
    def ver_ventas(cls):
        if not cls.ventas:
            print("No hay ventas registradas.")
        else:
            for i, venta in enumerate(cls.ventas, 1):
                print(f"\n--- Venta #{i} ---")
                print(venta)

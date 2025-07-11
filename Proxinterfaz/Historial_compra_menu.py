import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from HU.Venta import Venta

class HistorialComprasCliente:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Historial de Compras del Cliente")
        self.root.geometry("800x600")

        Venta.cargar_desde_json()

        self.setup_widgets()

    def setup_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Nombre del Cliente:").grid(row=0, column=0, padx=5)
        self.nombre_entry = tk.Entry(frame)
        self.nombre_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Fecha Inicio (dd/mm/aaaa):").grid(row=1, column=0, padx=5)
        self.fecha_inicio = tk.Entry(frame)
        self.fecha_inicio.grid(row=1, column=1, padx=5)

        tk.Label(frame, text="Fecha Fin (dd/mm/aaaa):").grid(row=2, column=0, padx=5)
        self.fecha_fin = tk.Entry(frame)
        self.fecha_fin.grid(row=2, column=1, padx=5)

        ttk.Button(frame, text="Buscar", command=self.buscar_historial).grid(row=3, column=0, columnspan=2, pady=10)

        self.resultado = tk.Text(self.root, width=100, height=25)
        self.resultado.pack(pady=10)

    def buscar_historial(self):
        self.resultado.delete(1.0, tk.END)
        nombre = self.nombre_entry.get().strip()
        desde_str = self.fecha_inicio.get().strip()
        hasta_str = self.fecha_fin.get().strip()

        if not nombre:
            messagebox.showerror("Error", "Debe ingresar el nombre del cliente")
            return

        ventas_cliente = Venta.filtrar_por_cliente(nombre)

        if desde_str and hasta_str:
            try:
                desde = datetime.strptime(desde_str, "%d/%m/%Y").date()
                hasta = datetime.strptime(hasta_str, "%d/%m/%Y").date()
                ventas_cliente = [v for v in ventas_cliente if desde <= v.fecha_venta.date() <= hasta]
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido")
                return

        if not ventas_cliente:
            self.resultado.insert(tk.END, "No hay compras registradas para este cliente.")
            return

        for i, venta in enumerate(ventas_cliente, 1):
            self.resultado.insert(tk.END, f"\n--- Compra #{i} ---\n")
            self.resultado.insert(tk.END, str(venta))
            self.resultado.insert(tk.END, "\n" + ("-" * 80) + "\n")

"""PedidosComponent - HU05
Ventana para registrar y visualizar pedidos
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from HU.Registrar_pedidos import GestorPedidos, Pedido  # ensure file name compatible
from ..configuracion import COLOR_PALETTE, FONTS, ICONS


class PedidosWindow:
    def __init__(self, parent):
        self.parent = parent
        self.colors = COLOR_PALETTE
        self.gestor = GestorPedidos()
        self.window = tk.Toplevel(parent)
        self.window.title("📑 Gestión de Pedidos")
        self.window.geometry("700x600")
        self.window.configure(bg=self.colors['light_gray'])
        self._center()
        self._build_ui()

    def _center(self):
        self.window.update_idletasks()
        w, h = 700, 600
        x = (self.window.winfo_screenwidth() // 2) - (w // 2)
        y = (self.window.winfo_screenheight() // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        header = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="📑 Registrar Pedido", font=FONTS['title'], bg=self.colors['primary'], fg=self.colors['white']).pack(expand=True)

        form_frame = tk.LabelFrame(self.window, text="🛒 Nuevo Pedido", font=FONTS['subtitle'], bg=self.colors['white'], fg=self.colors['dark_gray'], padx=20, pady=15)
        form_frame.pack(fill='x', padx=20, pady=10)

        # Campos
        tk.Label(form_frame, text="Cliente:", font=FONTS['label'], bg=self.colors['white']).grid(row=0, column=0, sticky='e', pady=5)
        self.cliente_entry = tk.Entry(form_frame, width=30)
        self.cliente_entry.grid(row=0, column=1, pady=5, padx=(10,0))

        tk.Label(form_frame, text="Producto:", font=FONTS['label'], bg=self.colors['white']).grid(row=1, column=0, sticky='e', pady=5)
        self.producto_var = tk.StringVar()
        self.producto_combo = ttk.Combobox(form_frame, textvariable=self.producto_var, state="readonly", width=28)
        self.producto_combo['values'] = list(self.gestor.inventario_dict.keys())
        self.producto_combo.grid(row=1, column=1, pady=5, padx=(10,0))

        tk.Label(form_frame, text="Cantidad:", font=FONTS['label'], bg=self.colors['white']).grid(row=2, column=0, sticky='e', pady=5)
        self.cantidad_entry = tk.Entry(form_frame, width=10)
        self.cantidad_entry.grid(row=2, column=1, pady=5, sticky='w', padx=(10,0))

        tk.Button(form_frame, text="Registrar Pedido", bg=self.colors['success'], fg=self.colors['white'], command=self._registrar).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(form_frame, text="Procesar a Venta", bg=self.colors['accent'], fg=self.colors['white'], command=self._procesar).grid(row=4, column=0, columnspan=2, pady=5)

        # Tabla pedidos
        table_frame = tk.LabelFrame(self.window, text="📋 Pedidos Registrados", font=FONTS['subtitle'], bg=self.colors['white'], fg=self.colors['dark_gray'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        columns = ("Cliente", "Producto", "Cantidad", "Fecha", "Estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.pack(fill='both', expand=True)
        self._refresh_table()

    # ------------- Acciones -------------
    def _registrar(self):
        cliente = self.cliente_entry.get().strip()
        prod = self.producto_var.get()
        cant_str = self.cantidad_entry.get().strip()
        if not cliente or not prod or not cant_str:
            messagebox.showerror("Campo obligatorio", "Por favor complete todos los campos.")
            return
        if not cant_str.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser numérica")
            return
        cantidad = int(cant_str)
        try:
            pedido = self.gestor.registrar_pedido(cliente, prod, cantidad)
            messagebox.showinfo("Éxito", f"Pedido registrado para {cliente}")
            self._refresh_table()
            self.cantidad_entry.delete(0, tk.END)
            self.cliente_entry.delete(0, tk.END)
            self.producto_var.set("")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.gestor.listar_pedidos():
            d = p.to_dict()
            self.tree.insert('', 'end', values=(d['cliente'], d['producto'], d['cantidad'], d['fecha'], d['estado'])) 

    def _procesar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Seleccionar", "Seleccione un pedido para procesar")
            return
        idx = int(sel[0])
        try:
            pedido = self.gestor.procesar_pedido(idx)
            messagebox.showinfo("Procesado", f"Pedido de {pedido.cliente} marcado como vendido")
            self._refresh_table()
        except Exception as e:
            messagebox.showerror("Error", str(e))


class PedidosComponent:
    """Componente embebible en Notebook para gestión de pedidos (HU05)."""
    def __init__(self, parent):
        self.parent = parent
        self.colors = COLOR_PALETTE
        self.gestor = GestorPedidos()

    def create_pedidos_tab(self, notebook):
        pedidos_frame = ttk.Frame(notebook)
        notebook.add(pedidos_frame, text=f"{ICONS.get('orders','📑')} Pedidos")

        # ----- Construir UI dentro del frame (reutiliza PedidosWindow logic) -----
        # Encabezado
        header = tk.Frame(pedidos_frame, bg='#f0f0f0', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="📑 Gestión de Pedidos", font=('Arial', 20, 'bold'), bg='#f0f0f0', fg='#333333').place(relx=0.5, rely=0.5, anchor='center')

        # Contenido scrollable
        content = tk.Frame(pedidos_frame, bg=self.colors['light_gray'])
        content.pack(fill='both', expand=True)

        # Reaprovechar PedidosWindow._build_ui creando widgets en content
        self._build_embedded(content)
        return pedidos_frame

    def _build_embedded(self, root):
        # Formulario
        form_frame = tk.LabelFrame(root, text="🛒 Nuevo Pedido", font=FONTS['subtitle'], bg=self.colors['white'], fg=self.colors['dark_gray'], padx=20, pady=15)
        form_frame.pack(fill='x', padx=20, pady=10)

        tk.Label(form_frame, text="Cliente:", font=FONTS['label'], bg=self.colors['white']).grid(row=0, column=0, sticky='e', pady=5)
        self.cliente_entry = tk.Entry(form_frame, width=30)
        self.cliente_entry.grid(row=0, column=1, pady=5, padx=(10,0))

        tk.Label(form_frame, text="Producto:", font=FONTS['label'], bg=self.colors['white']).grid(row=1, column=0, sticky='e', pady=5)
        self.producto_var = tk.StringVar()
        self.producto_combo = ttk.Combobox(form_frame, textvariable=self.producto_var, state="readonly", width=28)
        self.producto_combo['values'] = list(self.gestor.inventario_dict.keys())
        self.producto_combo.grid(row=1, column=1, pady=5, padx=(10,0))

        tk.Label(form_frame, text="Cantidad:", font=FONTS['label'], bg=self.colors['white']).grid(row=2, column=0, sticky='e', pady=5)
        self.cantidad_entry = tk.Entry(form_frame, width=10)
        self.cantidad_entry.grid(row=2, column=1, pady=5, sticky='w', padx=(10,0))

        tk.Button(form_frame, text="Registrar Pedido", bg=self.colors['success'], fg=self.colors['white'], command=self._registrar).grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(form_frame, text="Procesar a Venta", bg=self.colors['accent'], fg=self.colors['white'], command=self._procesar).grid(row=4, column=0, columnspan=2, pady=5)

        # Tabla de pedidos
        table_frame = tk.LabelFrame(root, text="📋 Pedidos Registrados", font=FONTS['subtitle'], bg=self.colors['white'], fg=self.colors['dark_gray'])
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        columns = ("Cliente", "Producto", "Cantidad", "Fecha", "Estado")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.pack(fill='both', expand=True)
        self._refresh_table()

    def _registrar(self):
        cliente = self.cliente_entry.get().strip()
        prod = self.producto_var.get()
        cant_str = self.cantidad_entry.get().strip()
        if not cliente or not prod or not cant_str:
            messagebox.showerror("Campo obligatorio", "Por favor complete todos los campos.")
            return
        if not cant_str.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser numérica")
            return
        cantidad = int(cant_str)
        try:
            self.gestor.registrar_pedido(cliente, prod, cantidad)
            messagebox.showinfo("Éxito", f"Pedido registrado para {cliente}")
            self._refresh_table()
            # limpiar
            self.cliente_entry.delete(0, tk.END)
            self.cantidad_entry.delete(0, tk.END)
            self.producto_var.set("")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, p in enumerate(self.gestor.listar_pedidos()):
            d = p.to_dict()
            self.tree.insert('', 'end', iid=str(idx), values=(d['cliente'], d['producto'], d['cantidad'], d['fecha'], d['estado']))

    def _procesar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Seleccionar", "Seleccione un pedido para procesar")
            return
        idx = int(sel[0])
        try:
            pedido = self.gestor.procesar_pedido(idx)
            messagebox.showinfo("Procesado", f"Pedido de {pedido.cliente} marcado como vendido")
            self._refresh_table()
        except Exception as e:
            messagebox.showerror("Error", str(e)) 
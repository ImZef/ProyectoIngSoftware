"""
Interfaz gráfica: Alertas de Stock Bajo (HU13)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

from ..configuracion import COLOR_PALETTE, FONTS, ICONS
from HU.AlertasStock import AlertasStockManager
from HU.Inventario import Inventario

class AlertasStockGUI:
    def __init__(self, parent, inventario: Inventario):
        self.parent = parent
        self.colors = COLOR_PALETTE
        self.inventario = inventario
        self.manager = AlertasStockManager(inventario)
        self.window = None

    # ------------ Ventana principal ------------
    def abrir(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚠️ Alertas de Stock Bajo")
        self.window.geometry("800x600")
        self.window.configure(bg=self.colors['light_gray'])
        self._center()
        self._crear_interfaz()
        self._cargar_datos()
        # Notificación inicial de nuevas alertas
        nuevos, _ = self.manager.detectar_nuevas_alertas()
        if nuevos:
            messagebox.showwarning("Nuevas alertas", f"⚠️ Hay {len(nuevos)} producto(s) con stock bajo que requieren atención inmediata.")

    def _center(self):
        self.window.update_idletasks()
        w, h = 800, 600
        x = (self.window.winfo_screenwidth() // 2) - (w // 2)
        y = (self.window.winfo_screenheight() // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")

    def _crear_interfaz(self):
        # Encabezado
        header = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="⚠️ Alertas de Inventario", font=FONTS['title'], bg=self.colors['primary'], fg=self.colors['white']).pack(expand=True)

        # Frame principal
        main = tk.Frame(self.window, bg=self.colors['light_gray'])
        main.pack(fill='both', expand=True, padx=20, pady=20)

        # Tabla de alertas
        columns = ("Código", "Producto", "Stock", "Umbral")
        self.tree = ttk.Treeview(main, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            anchor = 'center' if col in ("Código", "Stock", "Umbral") else 'w'
            self.tree.column(col, anchor=anchor, width=120)
        self.tree.column("Producto", width=350)
        vsb = ttk.Scrollbar(main, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        # Botón de configurar umbral
        btn_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        btn_frame.pack(fill='x')
        tk.Button(btn_frame, text="⚙️ Configurar Umbral", font=FONTS['label'], bg=self.colors['accent'], fg=self.colors['white'], command=self._abrir_dialogo_umbral).pack(pady=10)

    def _cargar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for alerta in self.manager.exportar_alertas_actuales():
            self.tree.insert('', 'end', values=(alerta['codigo'], alerta['nombre'], alerta['stock'], alerta['umbral']))

    # ------------ Configurar umbral -------------
    def _abrir_dialogo_umbral(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Selecciona", "Seleccione un producto de la lista")
            return
        item = self.tree.item(sel[0])
        codigo = item['values'][0]
        nombre = item['values'][1]
        umbral_actual = self.manager.obtener_umbral(codigo)

        dialog = tk.Toplevel(self.window)
        dialog.title("Configurar Umbral de Stock")
        dialog.geometry("400x200")
        dialog.configure(bg=self.colors['light_gray'])
        dialog.transient(self.window)
        dialog.grab_set()
        dialog_frame = tk.Frame(dialog, bg=self.colors['light_gray'])
        dialog_frame.pack(expand=True)
        tk.Label(dialog_frame, text=f"Producto: {nombre}", font=FONTS['subtitle'], bg=self.colors['light_gray']).pack(pady=10)
        tk.Label(dialog_frame, text="Nuevo umbral mínimo:", bg=self.colors['light_gray']).pack(pady=5)
        umbral_var = tk.StringVar(value=str(umbral_actual))
        entry = tk.Entry(dialog_frame, textvariable=umbral_var, width=10)
        entry.pack()

        def guardar():
            try:
                nuevo = int(umbral_var.get())
                self.manager.configurar_umbral_producto(codigo, nuevo)
                messagebox.showinfo("Éxito", "Umbral actualizado correctamente")
                dialog.destroy()
                self._cargar_datos()
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido")

        tk.Button(dialog_frame, text="Guardar", bg=self.colors['success'], fg=self.colors['white'], command=guardar).pack(pady=10) 
"""
Dialog windows for AgroVet Plus application.
"""

import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from HU.HistoriaClinica import HistoriaClinica
from HU.Producto import Producto
from .configuracion import COLOR_PALETTE, ICONS


class BaseDialog:
    """Clase base para ventanas de diálogo."""
    
    def __init__(self, parent, title, size="400x300"):
        self.parent = parent
        self.colors = COLOR_PALETTE
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        self.window.geometry(size)
        self.window.configure(bg=self.colors['light_gray'])
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)


class AddProductWindow(BaseDialog):
    """Ventana para agregar un nuevo producto al inventario."""
    
    def __init__(self, parent, inventario, callback):
        super().__init__(parent, "Agregar Nuevo Producto", "500x600")
        self.inventario = inventario
        self.callback = callback
        self.entries = {}
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets de la ventana."""
        # Título
        title_frame = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=f"{ICONS['add']} Agregar Nuevo Producto", 
                font=('Arial', 16, 'bold'), bg=self.colors['primary'], 
                fg=self.colors['white']).pack(expand=True)
        
        # Formulario
        form_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Campos del formulario
        fields = [
            ("Código:", "codigo"),
            ("Nombre:", "nombre"),
            ("Categoría:", "categoria"),
            ("Descripción:", "descripcion"),
            ("Precio:", "precio"),
            ("Cantidad:", "cantidad"),
            ("Fecha Vencimiento:", "fecha_vencimiento")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            tk.Label(form_frame, text=label_text, font=('Arial', 11, 'bold'), 
                    bg=self.colors['light_gray']).grid(row=i, column=0, sticky='w', pady=8, padx=(0, 10))
            
            if field_name == "descripcion":
                entry = tk.Text(form_frame, height=3, width=30, font=('Arial', 10))
            else:
                entry = tk.Entry(form_frame, font=('Arial', 10), width=30)
            
            entry.grid(row=i, column=1, sticky='ew', pady=8)
            self.entries[field_name] = entry
        
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Botones
        self.create_buttons()
        
    def create_buttons(self):
        """Crear botones de acción."""
        buttons_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        buttons_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Button(buttons_frame, text=f"{ICONS['save']} Guardar", command=self.save_product,
                 bg=self.colors['success'], fg=self.colors['white'], font=('Arial', 11, 'bold'),
                 relief='flat', padx=20, pady=8).pack(side='left', padx=(0, 10))
        
        tk.Button(buttons_frame, text=f"{ICONS['cancel']} Cancelar", command=self.window.destroy,
                 bg=self.colors['danger'], fg=self.colors['white'], font=('Arial', 11, 'bold'),
                 relief='flat', padx=20, pady=8).pack(side='left')
    
    def save_product(self):
        """Guardar el producto."""
        try:
            # Obtener valores
            codigo = int(self.entries["codigo"].get())
            nombre = self.entries["nombre"].get().strip()
            categoria = self.entries["categoria"].get().strip()
            descripcion = self.entries["descripcion"].get("1.0", tk.END).strip()
            precio = float(self.entries["precio"].get())
            cantidad = int(self.entries["cantidad"].get())
            fecha_vencimiento = self.entries["fecha_vencimiento"].get().strip()
            
            # Validaciones
            if not all([nombre, categoria, descripcion]):
                messagebox.showerror("Error", "Todos los campos son requeridos")
                return
            
            # Verificar si el código ya existe
            if self.inventario.buscar_por_codigo(codigo):
                messagebox.showerror("Error", "Ya existe un producto con ese código")
                return
            
            # Crear producto
            producto = Producto(codigo, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento)
            self.inventario.agregar_producto(producto)
            self.inventario.guardar_en_json()
            
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.callback()
            self.window.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor verifique que los números sean válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar producto: {str(e)}")


class UpdateStockWindow(BaseDialog):
    """Ventana para actualizar el stock de un producto existente."""
    
    def __init__(self, parent, inventario, codigo, callback):
        super().__init__(parent, "Actualizar Stock", "400x300")
        self.inventario = inventario
        self.codigo = codigo
        self.callback = callback
        self.producto = inventario.buscar_por_codigo(int(codigo))
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets de la ventana."""
        # Título
        title_frame = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=f"{ICONS['inventory']} Actualizar Stock", 
                font=('Arial', 16, 'bold'), bg=self.colors['primary'], 
                fg=self.colors['white']).pack(expand=True)
        
        # Información del producto
        info_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        info_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(info_frame, text=f"Producto: {self.producto.get_nombre()}", 
                font=('Arial', 12, 'bold'), bg=self.colors['light_gray']).pack(anchor='w')
        tk.Label(info_frame, text=f"Stock actual: {self.producto.get_cantidad()}", 
                font=('Arial', 11), bg=self.colors['light_gray']).pack(anchor='w')
        
        # Formulario
        form_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        form_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(form_frame, text="Nueva cantidad:", font=('Arial', 11, 'bold'), 
                bg=self.colors['light_gray']).grid(row=0, column=0, sticky='w', pady=5)
        
        self.cantidad_entry = tk.Entry(form_frame, font=('Arial', 10), width=20)
        self.cantidad_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        tk.Label(form_frame, text="Motivo:", font=('Arial', 11, 'bold'), 
                bg=self.colors['light_gray']).grid(row=1, column=0, sticky='w', pady=5)
        
        self.motivo_entry = tk.Entry(form_frame, font=('Arial', 10), width=20)
        self.motivo_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Botones
        self.create_buttons()
        
    def create_buttons(self):
        """Crear botones de acción."""
        buttons_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        buttons_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Button(buttons_frame, text=f"{ICONS['save']} Actualizar", command=self.update_stock,
                 bg=self.colors['success'], fg=self.colors['white'], font=('Arial', 11, 'bold'),
                 relief='flat', padx=20, pady=8).pack(side='left', padx=(0, 10))
        
        tk.Button(buttons_frame, text=f"{ICONS['cancel']} Cancelar", command=self.window.destroy,
                 bg=self.colors['danger'], fg=self.colors['white'], font=('Arial', 11, 'bold'),
                 relief='flat', padx=20, pady=8).pack(side='left')
    
    def update_stock(self):
        """Actualizar el stock del producto."""
        try:
            nueva_cantidad = int(self.cantidad_entry.get())
            motivo = self.motivo_entry.get().strip()
            
            if not motivo:
                messagebox.showerror("Error", "El motivo es requerido")
                return
            
            self.inventario.actualizar_stock(int(self.codigo), nueva_cantidad, motivo)
            messagebox.showinfo("Éxito", "Stock actualizado correctamente")
            self.callback()
            self.window.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar stock: {str(e)}")


class HistoryWindow(BaseDialog):
    """Ventana para visualizar el historial de movimientos de stock."""
    
    def __init__(self, parent, inventario):
        super().__init__(parent, "Historial de Movimientos", "800x600")
        self.inventario = inventario
        self.create_widgets()
    
    def create_widgets(self):
        """Crear los widgets de la ventana."""
        # Título
        title_frame = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=f"{ICONS['history']} Historial de Movimientos de Stock", 
                font=('Arial', 16, 'bold'), bg=self.colors['primary'], 
                fg=self.colors['white']).pack(expand=True)
        
        # Área de texto con scroll
        text_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        text_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.text_area = scrolledtext.ScrolledText(text_frame, font=('Courier', 10), 
                                                  bg=self.colors['white'], fg=self.colors['dark_gray'])
        self.text_area.pack(fill='both', expand=True)
        
        # Cargar historial
        self.load_history()
        
        # Botón cerrar
        tk.Button(self.window, text="Cerrar", command=self.window.destroy,
                 bg=self.colors['dark_gray'], fg=self.colors['white'], font=('Arial', 11, 'bold'),
                 relief='flat', padx=20, pady=8).pack(pady=10)
    
    def load_history(self):
        """Cargar el historial de movimientos."""
        try:
            with open("historial_stock.json", "r") as archivo:
                historial = json.load(archivo)
                
                if not historial:
                    self.text_area.insert(tk.END, "No hay movimientos registrados.")
                    return
                
                self.text_area.insert(tk.END, "=== HISTORIAL DE MOVIMIENTOS DE STOCK ===\n\n")
                
                for registro in reversed(historial):  # Mostrar más recientes primero
                    self.text_area.insert(tk.END, f"Fecha: {registro['fecha']}\n")
                    self.text_area.insert(tk.END, f"Producto: {registro['nombre_producto']}\n")
                    self.text_area.insert(tk.END, f"Cambio: {registro['stock_anterior']} → {registro['nuevo_stock']}\n")
                    self.text_area.insert(tk.END, f"Motivo: {registro['motivo']}\n")
                    self.text_area.insert(tk.END, "-" * 50 + "\n\n")
                    
        except FileNotFoundError:
            self.text_area.insert(tk.END, "No hay historial de movimientos registrado.")


class ClinicalEntryWindow(BaseDialog):
    """Ventana para registrar o actualizar un historial clínico."""
    
    def __init__(self, parent, callback):
        super().__init__(parent, "Registrar/Actualizar Historial Clínico", "450x550")
        self.callback = callback
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        """Crear los widgets de la ventana."""
        # Título
        title_frame = tk.Frame(self.window, bg=self.colors['primary'], height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=f"{ICONS['clinical']} Historial Clínico", 
                font=('Arial', 16, 'bold'), bg=self.colors['primary'], 
                fg=self.colors['white']).pack(expand=True)
        
        # Formulario
        form_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        form_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        labels = ["ID Cliente:", "Nombre Cliente:", "Nombre Mascota:", 
                  "Diagnóstico:", "Tratamiento:", "Comentarios (opcional):"]
        
        for i, lbl in enumerate(labels):
            tk.Label(form_frame, text=lbl, font=('Arial', 11, 'bold'), 
                    bg=self.colors['light_gray']).grid(row=i, column=0, sticky='w', pady=5)
            
            if lbl.startswith("Comentarios"):
                ent = tk.Text(form_frame, height=3, width=30, font=('Arial', 10))
                ent.grid(row=i, column=1, pady=5)
            else:
                ent = tk.Entry(form_frame, font=('Arial', 10), width=30)
                ent.grid(row=i, column=1, pady=5)
            self.entries[lbl] = ent
        
        # Botones
        self.create_buttons()
        
    def create_buttons(self):
        """Crear botones de acción."""
        buttons_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        buttons_frame.pack(fill='x', pady=10)
        
        tk.Button(buttons_frame, text=f"{ICONS['save']} Guardar", command=self.save, 
                 bg=self.colors['success'], fg=self.colors['white'], font=('Arial', 11, 'bold'), 
                 relief='flat').pack(side='left', padx=10)
        
        tk.Button(buttons_frame, text=f"{ICONS['cancel']} Cancelar", command=self.window.destroy, 
                 bg=self.colors['danger'], fg=self.colors['white'], font=('Arial', 11, 'bold'), 
                 relief='flat').pack(side='left')

    def save(self):
        """Guardar el registro clínico."""
        try:
            id_cliente = self.entries["ID Cliente:"].get().strip()
            if not id_cliente.isdigit(): 
                raise ValueError("ID debe ser numérico")
            
            nombre = self.entries["Nombre Cliente:"].get().strip()
            mascota = self.entries["Nombre Mascota:"].get().strip()
            diag = self.entries["Diagnóstico:"].get().strip()
            trat = self.entries["Tratamiento:"].get().strip()
            coment = self.entries["Comentarios (opcional):"].get("1.0", tk.END).strip()
            
            if not diag or not trat: 
                raise ValueError("Diagnóstico y Tratamiento son obligatorios")
            
            # Buscar historial existente
            hist = HistoriaClinica.buscar_historial(id_cliente)
            if not hist:
                messagebox.showerror("Error", "ID no existente. No se puede actualizar historial.")
                return
            
            # Registrar diagnóstico
            hist.registrar_diagnostico(diag, trat, coment)
            HistoriaClinica.guardar_historiales()
            messagebox.showinfo("Éxito", "Registro clínico guardado correctamente")
            self.callback()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

"""
Dialog windows for AgroVet Plus application.
"""

import json
import tkinter as tk
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

# -------- Intento de importar selector de fecha -------------
try:
    from tkcalendar import DateEntry  # type: ignore
except ImportError:
    DateEntry = None  # Fallback a Entry si no está instalado

from HU.HistoriaClinica import HistoriaClinica
from HU.Producto import Producto
from ..configuracion import COLOR_PALETTE, ICONS, FONTS


class BaseDialog:
    """Clase base para ventanas de diálogo."""
    
    def __init__(self, parent, title, size="400x300"):
        self.parent = parent
        self.colors = COLOR_PALETTE
        self.window = tk.Toplevel(parent)
        self.window.title(title)
        # Establecer tamaño
        self.window.geometry(size)
        # Centrar la ventana en la pantalla
        self._center_window(size)
        self.window.configure(bg=self.colors['light_gray'])
        self.window.transient(parent)
        self.window.grab_set()
        self.window.resizable(False, False)

    # ---------------- Utilidades -----------------
    def _center_window(self, size_str):
        """Centrar la ventana según el tamaño proporcionado (formato WxH)."""
        try:
            if 'x' in size_str:
                w, h = map(int, size_str.lower().split('x'))
            else:
                # Fallback: usar winfo_reqwidth/height tras actualización
                self.window.update_idletasks()
                w = self.window.winfo_reqwidth()
                h = self.window.winfo_reqheight()
        except Exception:
            self.window.update_idletasks()
            w = self.window.winfo_reqwidth()
            h = self.window.winfo_reqheight()

        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w // 2) - (w // 2)
        y = (screen_h // 2) - (h // 2)
        self.window.geometry(f"{w}x{h}+{x}+{y}")


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
        """Crear botones de acción usando tk.Button para mostrar colores definidos."""
        buttons_frame = tk.Frame(self.window, bg=self.colors['light_gray'])
        buttons_frame.pack(fill='x', padx=10, pady=10)
        # Botón Actualizar destacado en verde con tamaño fijo para mostrar texto
        btn_update = tk.Button(buttons_frame,
                               text=f"{ICONS['save']} Actualizar Stock",
                               command=self.update_stock,
                               bg=self.colors['success'], fg=self.colors['white'],
                               font=FONTS['label'], relief='raised', bd=2,
                               width=15, height=20)
        btn_update.pack(side='left', padx=(0, 10))
        # Botón Cancelar destacado en rojo con tamaño fijo
        btn_cancel = tk.Button(buttons_frame,
                               text=f"{ICONS['cancel']} Cancelar",
                               command=self.window.destroy,
                               bg=self.colors['danger'], fg=self.colors['white'],
                               font=FONTS['label'], relief='raised', bd=2,
                               width=15, height=2)
        btn_cancel.pack(side='left')
    
    def update_stock(self):
        """Actualizar el stock del producto."""
        try:
            nueva_cantidad = int(self.cantidad_entry.get())
            # No permitir cantidades negativas
            if nueva_cantidad < 0:
                messagebox.showerror("Error", "La cantidad no puede ser negativa")
                return
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
            with open("db/historial_stock.json", "r") as archivo:
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
    
    def __init__(self, parent, callback, auto_id=False):
        super().__init__(parent, "Registrar/Actualizar Historial Clínico", "450x550")
        self.callback = callback
        self.auto_id = auto_id
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
                # Autocompletar y bloquear ID si auto_id
            self.entries[lbl] = ent

        if self.auto_id:
            from HU.HistoriaClinica import HistoriaClinica
            next_id = HistoriaClinica.get_next_id()
            self.entries["ID Cliente:"].insert(0, str(next_id))
            self.entries["ID Cliente:"].config(state='disabled')
        
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

            # Validaciones HU09
            if not nombre:
                raise ValueError("El nombre del cliente es obligatorio")
            if not mascota:
                raise ValueError("El nombre de la mascota es obligatorio")
            if not diag:
                raise ValueError("El diagnóstico es obligatorio")
            if not trat:
                raise ValueError("El tratamiento es obligatorio")
            
            # Si es un nuevo historial (ID automático), crearlo directamente
            if self.auto_id:
                hist = HistoriaClinica(id_cliente, nombre, mascota)
                HistoriaClinica.historiales.append(hist)  # Añadir explícitamente a la lista
            else:
                # Si se actualiza, buscar y, si no existe, preguntar para crearlo
                hist = HistoriaClinica.buscar_historial(id_cliente)
                if not hist:
                    if messagebox.askyesno("Nuevo Historial", "ID no existente. ¿Desea crear un nuevo historial para este cliente?"):
                        hist = HistoriaClinica(id_cliente, nombre, mascota)
                        HistoriaClinica.historiales.append(hist)  # Añadir explícitamente a la lista
                    else:
                        return
            
            # Registrar diagnóstico
            hist.registrar_diagnostico(diag, trat, coment)
            HistoriaClinica.guardar_historiales()
            messagebox.showinfo("Éxito", "Registro clínico guardado correctamente")
            self.callback()
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))


class PurchaseHistoryWindow(BaseDialog):
    """Ventana para visualizar el historial de compras de un cliente."""

    def __init__(self, parent):
        super().__init__(parent, "Historial de Compras del Cliente", "800x650")
        from HU.Venta import Venta  # Importación diferida para evitar ciclos
        self.Venta = Venta
        # Cargar las ventas desde archivo (en caso de no estar cargadas)
        try:
            self.Venta.cargar_desde_json()
        except Exception:
            pass
        self.create_widgets()

    def create_widgets(self):
        frm = tk.Frame(self.window, bg=self.colors['light_gray'])
        frm.pack(fill='both', expand=True, padx=20, pady=20)

        # --------- Formulario de búsqueda ---------
        form = tk.LabelFrame(frm, text=f"{ICONS['search']} Buscar Compras", bg=self.colors['white'], fg=self.colors['dark_gray'])
        form.pack(fill='x', pady=(0, 15))

        tk.Label(form, text="Cliente:", bg=self.colors['white']).grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.clientes_combo = ttk.Combobox(form, width=28, state="readonly")
        self.clientes_combo.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self._refresh_client_list()

        tk.Label(form, text="Fecha Inicio (dd/mm/aaaa):", bg=self.colors['white']).grid(row=1, column=0, sticky='e', padx=5, pady=5)
        if DateEntry:
            self.inicio_entry = DateEntry(form, date_pattern='dd/mm/yyyy', width=12)
        else:
            self.inicio_entry = tk.Entry(form, width=15)
        self.inicio_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        tk.Label(form, text="Fecha Fin (dd/mm/aaaa):", bg=self.colors['white']).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        if DateEntry:
            self.fin_entry = DateEntry(form, date_pattern='dd/mm/yyyy', width=12)
        else:
            self.fin_entry = tk.Entry(form, width=15)
        self.fin_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        tk.Button(form, text=f"{ICONS['search']} Buscar", bg=self.colors['primary'], fg=self.colors['white'], command=self.search).grid(row=3, column=0, columnspan=2, pady=10)

        # --------- Tabla de resultados ---------
        table_frame = ttk.Frame(frm)
        table_frame.pack(fill='both', expand=True)

        columns = ("Fecha", "Total", "Forma Pago")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Doble clic para ver detalle
        self.tree.bind('<Double-1>', self._on_double_click)

    def search(self):
        from datetime import datetime
        # Obtener cliente seleccionado
        cliente_sel = self.clientes_combo.get().strip()
        nombre = cliente_sel
        if not nombre:
            messagebox.showerror("Error", "Debe seleccionar un cliente")
            return
        ventas_cliente = self.Venta.filtrar_por_cliente(nombre)

        # Filtro por fechas
        inicio_str = self._get_date_str(self.inicio_entry)
        fin_str = self._get_date_str(self.fin_entry)

        if inicio_str and fin_str:
            try:
                inicio = datetime.strptime(inicio_str, "%d/%m/%Y").date()
                fin = datetime.strptime(fin_str, "%d/%m/%Y").date()
                ventas_cliente = [v for v in ventas_cliente if inicio <= v.fecha_venta.date() <= fin]
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido")
                return

        # Ordenar por fecha descendente
        ventas_cliente.sort(key=lambda v: v.fecha_venta, reverse=True)

        self._load_table(ventas_cliente)

    # --------------------------------------------------
    def _get_date_str(self, widget):
        if DateEntry and isinstance(widget, DateEntry):
            return widget.get()
        return widget.get().strip()

    def _refresh_client_list(self):
        """Carga nombres únicos de clientes en el combobox."""
        nombres = sorted({v.cliente for v in self.Venta.ventas})
        self.clientes_combo['values'] = nombres

    def _load_table(self, ventas):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not ventas:
            messagebox.showinfo("Sin resultados", "No hay compras registradas para los criterios dados.")
            return
        for idx, v in enumerate(ventas, 1):
            fecha_str = v.fecha_venta.strftime("%d/%m/%Y %H:%M:%S")
            self.tree.insert('', 'end', iid=str(idx), values=(fecha_str, f"${v.total():,.0f}", v.forma_pago), tags=(idx,))
        # Guardar referencia para detalle
        self._ventas_mostradas = ventas

    def _on_double_click(self, event):
        item_id = self.tree.selection()
        if not item_id:
            return
        index = int(item_id[0]) - 1
        venta = self._ventas_mostradas[index]
        self._show_detail_window(venta)

    def _show_detail_window(self, venta):
        """Muestra un Toplevel con el detalle de la venta."""
        win = tk.Toplevel(self.window)
        win.title("Detalle de Compra")
        win.geometry("500x400")
        text = tk.Text(win, bg=self.colors['white'], fg=self.colors['dark_gray'])
        text.pack(fill='both', expand=True)
        text.insert(tk.END, str(venta))
        text.config(state='disabled')

# ==================== Nueva ventana: Registrar Cliente y Necesidad (HU14) ====================
class RegisterNeedWindow(BaseDialog):
    """Ventana para que el Auxiliar de Ventas registre la necesidad de un cliente (HU14)."""
    def __init__(self, parent, inventario, default_tipo='venta', allow_tipo_change=True):
        super().__init__(parent, "Registrar Cliente y Necesidad", "500x550")
        self.inventario = inventario
        self.default_tipo = default_tipo
        self.allow_tipo_change = allow_tipo_change
        self.create_widgets()

    def create_widgets(self):
        frm = tk.Frame(self.window, bg=self.colors['white'])
        frm.pack(fill='both', expand=True, padx=20, pady=20)

        # ===== Datos del Cliente =====
        tk.Label(frm, text="👤 Nombre Cliente:", bg=self.colors['white']).grid(row=0, column=0, sticky='e', pady=5)
        self.cliente_entry = tk.Entry(frm, width=30)
        self.cliente_entry.grid(row=0, column=1, sticky='w', pady=5)

        tk.Label(frm, text="📞 Contacto (opcional):", bg=self.colors['white']).grid(row=1, column=0, sticky='e', pady=5)
        self.contacto_entry = tk.Entry(frm, width=30)
        self.contacto_entry.grid(row=1, column=1, sticky='w', pady=5)

        # ===== Tipo de Necesidad =====
        tk.Label(frm, text="🔎 Tipo Necesidad:", bg=self.colors['white']).grid(row=2, column=0, sticky='e', pady=5)
        self.tipo_var = tk.StringVar(value=self.default_tipo)
        state_combo = 'readonly' if self.allow_tipo_change else 'disabled'
        tipo_combo = ttk.Combobox(frm, textvariable=self.tipo_var, state=state_combo,
                                  values=['venta', 'consulta'], width=28)
        tipo_combo.grid(row=2, column=1, sticky='w', pady=5)
        tipo_combo.bind('<<ComboboxSelected>>', self._on_tipo_change)

        # ===== Frame para secciones dinámicas =====
        self.dynamic_frame = tk.Frame(frm, bg=self.colors['white'])
        self.dynamic_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        # Crear la sección adecuada según tipo por defecto
        if self.default_tipo == 'venta':
            self._create_venta_widgets()
        else:
            self._create_consulta_widgets()

        # ===== Botones =====
        btn_frame = tk.Frame(frm, bg=self.colors['white'])
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text=f"{ICONS['save']} Guardar", bg=self.colors['success'], fg=self.colors['white'],
                  command=self._on_save).pack(side='left', padx=10)
        tk.Button(btn_frame, text=f"{ICONS['cancel']} Cancelar", bg=self.colors['danger'], fg=self.colors['white'],
                  command=self.window.destroy).pack(side='left', padx=10)

    # ----------------- Secciones dinámicas -----------------
    def _clear_dynamic(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

    def _create_venta_widgets(self):
        self._clear_dynamic()
        tk.Label(self.dynamic_frame, text="📦 Producto:", bg=self.colors['white']).grid(row=0, column=0, sticky='e', pady=5)
        self.producto_var = tk.StringVar()
        disponibles = [p for p in self.inventario.productos if p.get_cantidad() > 0]
        self.producto_combo = ttk.Combobox(self.dynamic_frame, textvariable=self.producto_var, state='readonly',
                                           values=[f"{p.nombre} - Stock:{p.get_cantidad()}" for p in disponibles], width=28)
        self.producto_combo.grid(row=0, column=1, sticky='w', pady=5)

        tk.Label(self.dynamic_frame, text="🔢 Cantidad:", bg=self.colors['white']).grid(row=1, column=0, sticky='e', pady=5)
        self.cantidad_entry = tk.Entry(self.dynamic_frame, width=10)
        self.cantidad_entry.grid(row=1, column=1, sticky='w', pady=5)

        tk.Label(self.dynamic_frame, text="💳 Forma Pago:", bg=self.colors['white']).grid(row=2, column=0, sticky='e', pady=5)
        self.pago_var = tk.StringVar(value='efectivo')
        self.pago_combo = ttk.Combobox(self.dynamic_frame, textvariable=self.pago_var, state='readonly',
                                       values=['efectivo', 'tarjeta'], width=12)
        self.pago_combo.grid(row=2, column=1, sticky='w', pady=5)

    def _create_consulta_widgets(self):
        self._clear_dynamic()
        tk.Label(self.dynamic_frame, text="📝 Descripción Consulta:", bg=self.colors['white']).grid(row=0, column=0, sticky='nw', pady=5)
        self.descripcion_text = tk.Text(self.dynamic_frame, width=35, height=8)
        self.descripcion_text.grid(row=0, column=1, pady=5, sticky='w')

    def _on_tipo_change(self, _event=None):
        if self.tipo_var.get() == 'venta':
            self._create_venta_widgets()
        else:
            self._create_consulta_widgets()

    # ----------------- Guardar -----------------
    def _on_save(self):
        from datetime import datetime
        cliente = self.cliente_entry.get().strip()
        if not cliente:
            messagebox.showerror("Error", "El nombre del cliente es obligatorio")
            return

        tipo = self.tipo_var.get()
        data = {
            "cliente": cliente,
            "contacto": self.contacto_entry.get().strip(),
            "tipo": tipo,
            "fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }

        if tipo == 'venta':
            # Validar producto y cantidad
            if not self.producto_var.get():
                messagebox.showerror("Error", "Seleccione un producto")
                return
            try:
                cantidad = int(self.cantidad_entry.get())
                if cantidad <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Cantidad inválida")
                return
            prod_nombre = self.producto_var.get().split(' - Stock')[0]
            producto = next((p for p in self.inventario.productos if p.nombre == prod_nombre), None)
            if producto is None:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            if cantidad > producto.get_cantidad():
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto.get_cantidad()}")
                return

            data.update({
                "producto_codigo": producto.get_codigo(),
                "producto_nombre": producto.get_nombre(),
                "cantidad": cantidad,
                "forma_pago": self.pago_var.get()
            })
        else:
            descripcion = self.descripcion_text.get("1.0", tk.END).strip()
            if not descripcion:
                messagebox.showerror("Error", "La descripción es obligatoria")
                return
            data["descripcion"] = descripcion

        # -------- Resumen antes de confirmar --------
        resumen = f"Cliente: {cliente}\nTipo: {('Compra' if tipo=='venta' else 'Consulta')}\n"
        if tipo == 'venta':
            resumen += f"Producto: {data['producto_nombre']}\nCantidad: {data['cantidad']}\nPago: {data['forma_pago']}\n"
        else:
            resumen += f"Descripción: {data['descripcion'][:50]}...\n"
        resumen += "¿Confirmar registro?"

        if not messagebox.askyesno("Confirmar", resumen):
            return

        # -------- Guardar en JSON --------
        try:
            with open("db/solicitudes.json", "r", encoding="utf-8") as f:
                solicitudes = json.load(f)
        except FileNotFoundError:
            solicitudes = []
        except json.decoder.JSONDecodeError:
            solicitudes = []

        solicitudes.append(data)
        with open("db/solicitudes.json", "w", encoding="utf-8") as f:
            json.dump(solicitudes, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Éxito", "Solicitud registrada correctamente")
        self.window.destroy()

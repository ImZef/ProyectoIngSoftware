"""
Sales management component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import json
from datetime import datetime

from ..configuracion import COLOR_PALETTE, FONTS, ICONS


class SalesComponent:
    """Componente para la gestión de ventas."""
    
    def __init__(self, parent, inventario, refresh_callback=None):
        self.parent = parent
        self.inventario = inventario
        self.refresh_callback = refresh_callback
        self.colors = COLOR_PALETTE
        
        # Variables de interfaz
        self.cliente_entry = None
        self.producto_var = None
        self.producto_combo = None
        self.pago_var = None
        self.pago_combo = None
        self.cantidad_entry = None
        self.carrito_text = None
        self.carrito_items = []
        
    def create_sales_tab(self, notebook):
        """Crear la pestaña de ventas."""
        sales_frame = ttk.Frame(notebook)
        notebook.add(sales_frame, text=f"{ICONS.get('sales', '💰')} Ventas")
        
        # Encabezado centrado - Similar al diseño de otros componentes
        header_frame = tk.Frame(sales_frame, bg='#f0f0f0', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="💰 Sistema de Ventas",
                              font=('Arial', 24, 'bold'),
                              bg='#f0f0f0',
                              fg='#333333')
        title_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Frame principal
        main_frame = tk.Frame(sales_frame, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Frame de contenido con scroll
        canvas = tk.Canvas(main_frame, bg=self.colors['white'])
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enlazar scroll con rueda del ratón
        self._bind_mousewheel(canvas)

        # Frame para la funcionalidad de ventas
        self.create_sales_functionality(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return sales_frame
        
    def create_sales_functionality(self, parent):
        """Crear la funcionalidad de ventas."""
        # Frame principal para centrar contenido
        main_container = tk.Frame(parent, bg=self.colors['white'])
        main_container.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Frame de nueva venta - Centrado y con mejor proporción
        new_sale_frame = tk.LabelFrame(main_container,
                                      text="🛒 Nueva Venta",
                                      font=FONTS['subtitle'],
                                      bg=self.colors['white'],
                                      fg=self.colors['dark_gray'],
                                      padx=20,
                                      pady=15,
                                      relief='raised',
                                      bd=3)
        new_sale_frame.pack(expand=True, anchor='n', pady=(0, 20))
        
        # Frame interno para centrar el formulario
        form_frame = tk.Frame(new_sale_frame, bg=self.colors['white'])
        form_frame.pack(pady=10, anchor='center')
        
        # Configurar grid para el formulario con mejor espaciado
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Cliente
        cliente_label = tk.Label(form_frame, text="👤 Cliente:", font=FONTS['label'],
                bg=self.colors['white'], fg=self.colors['dark_gray'])
        cliente_label.grid(row=0, column=0, sticky='e', padx=(0, 15), pady=10)
        
        self.cliente_entry = tk.Entry(form_frame, font=FONTS['text'], width=35, 
                                     relief='solid', bd=1)
        self.cliente_entry.grid(row=0, column=1, sticky='w', pady=10)
        
        # Producto
        producto_label = tk.Label(form_frame, text="📦 Producto:", font=FONTS['label'],
                bg=self.colors['white'], fg=self.colors['dark_gray'])
        producto_label.grid(row=1, column=0, sticky='e', padx=(0, 15), pady=10)
        
        # Combobox para productos
        self.producto_var = tk.StringVar()
        self.producto_combo = ttk.Combobox(form_frame, textvariable=self.producto_var,
                                          font=FONTS['text'], width=33, state="readonly")
        
        # Llenar combobox con productos del inventario (solo disponibles)
        self._refresh_productos_combo()
        self.producto_combo.grid(row=1, column=1, sticky='w', pady=10)
        
        # Forma de pago
        pago_label = tk.Label(form_frame, text="💳 Forma de pago:", font=FONTS['label'],
                bg=self.colors['white'], fg=self.colors['dark_gray'])
        pago_label.grid(row=2, column=0, sticky='e', padx=(0, 15), pady=10)

        self.pago_var = tk.StringVar()
        self.pago_combo = ttk.Combobox(form_frame, textvariable=self.pago_var,
                                       values=["efectivo", "tarjeta"], state="readonly",
                                       font=FONTS['text'], width=33)
        self.pago_combo.grid(row=2, column=1, sticky='w', pady=10)
        self.pago_combo.set("efectivo")

        # Cantidad
        cantidad_label = tk.Label(form_frame, text="🔢 Cantidad:", font=FONTS['label'],
                bg=self.colors['white'], fg=self.colors['dark_gray'])
        cantidad_label.grid(row=3, column=0, sticky='e', padx=(0, 15), pady=10)

        self.cantidad_entry = tk.Entry(form_frame, font=FONTS['text'], width=15,
                                      relief='solid', bd=1)
        self.cantidad_entry.grid(row=3, column=1, sticky='w', pady=10)
        
        # Frame para botones - Centrado y con mejor distribución
        button_container = tk.Frame(new_sale_frame, bg=self.colors['white'])
        button_container.pack(pady=20, anchor='center')
        
        # Primera fila de botones
        button_row1 = tk.Frame(button_container, bg=self.colors['white'])
        button_row1.pack(pady=5, anchor='center')
        
        btn_agregar = tk.Button(button_row1,
                 text="🛒 Agregar al Carrito",
                 font=FONTS['label'],
                 bg=self.colors['accent'],
                 fg=self.colors['white'],
                 command=self.agregar_al_carrito,
                 padx=20,
                 pady=8,
                 relief='raised',
                 bd=2,
                 cursor='hand2')
        btn_agregar.pack(side='left', padx=8)
 
        btn_solicitud = tk.Button(button_row1,
                 text="📄 Registrar Consulta",
                 font=FONTS['label'],
                 bg=self.colors['primary'],
                 fg=self.colors['white'],
                 command=self.registrar_solicitud,
                 padx=20,
                 pady=8,
                 relief='raised',
                 bd=2,
                 cursor='hand2')
        btn_solicitud.pack(side='left', padx=8)

        # Segunda fila de botones
        button_row2 = tk.Frame(button_container, bg=self.colors['white'])
        button_row2.pack(pady=5, anchor='center')

        btn_procesar = tk.Button(button_row2,
                 text="💳 Procesar Venta",
                 font=FONTS['label'],
                 bg=self.colors['success'],
                 fg=self.colors['white'],
                 command=self.procesar_venta,
                 padx=20,
                 pady=8,
                 relief='raised',
                 bd=2,
                 cursor='hand2')
        btn_procesar.pack(side='left', padx=8)
        
        btn_historial = tk.Button(button_row2,
                 text="📜 Historial Cliente",
                 font=FONTS['label'],
                 bg=self.colors['secondary'],
                 fg=self.colors['dark_gray'],
                 command=self.open_purchase_history,
                 padx=20,
                 pady=8,
                 relief='raised',
                 bd=2,
                 cursor='hand2')
        btn_historial.pack(side='left', padx=8)
        
        # Botón Pedidos

        
        # Frame del carrito - Mejorado y proporcional
        carrito_frame = tk.LabelFrame(main_container,
                                     text="🛍️ Carrito de Compras",
                                     font=FONTS['subtitle'],
                                     bg=self.colors['white'],
                                     fg=self.colors['dark_gray'],
                                     padx=20,
                                     pady=15,
                                     relief='raised',
                                     bd=3)
        carrito_frame.pack(fill='both', expand=True)
        
        # Frame interno del carrito con padding
        carrito_content = tk.Frame(carrito_frame, bg=self.colors['white'])
        carrito_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Lista del carrito con scroll mejorado
        carrito_scroll_frame = tk.Frame(carrito_content, bg=self.colors['white'])
        carrito_scroll_frame.pack(fill='both', expand=True)
        
        # Scrollbar para el carrito
        carrito_scrollbar = ttk.Scrollbar(carrito_scroll_frame)
        carrito_scrollbar.pack(side='right', fill='y')
        
        # Text widget para el carrito
        self.carrito_text = tk.Text(carrito_scroll_frame, height=12, font=FONTS['text'],
                                   bg=self.colors['light_gray'], fg=self.colors['dark_gray'],
                                   relief='solid', bd=1,
                                   yscrollcommand=carrito_scrollbar.set)
        self.carrito_text.pack(side='left', fill='both', expand=True)
        
        carrito_scrollbar.config(command=self.carrito_text.yview)
        
        # Inicializar carrito vacío
        self.carrito_items = []
        self.actualizar_carrito_display()
        
    def agregar_al_carrito(self):
        """Agregar producto al carrito."""
        try:
            if not self.cliente_entry.get().strip():
                messagebox.showerror("Error", "⚠️ Debe ingresar el nombre del cliente")
                return
                
            if not self.producto_var.get():
                messagebox.showerror("Error", "⚠️ Debe seleccionar un producto")
                return
                
            cantidad = int(self.cantidad_entry.get())
            if cantidad <= 0:
                messagebox.showerror("Error", "⚠️ La cantidad debe ser mayor a 0")
                return
            
            # Obtener producto seleccionado
            producto_seleccionado = None
            producto_nombre = self.producto_var.get().split(' - $')[0]
            
            for producto in self.inventario.productos:
                if producto.nombre == producto_nombre:
                    producto_seleccionado = producto
                    break
                    
            if producto_seleccionado and cantidad <= producto_seleccionado.get_cantidad():
                # Agregar al carrito
                item = {
                    'producto': producto_seleccionado,
                    'cantidad': cantidad,
                    'subtotal': producto_seleccionado.precio * cantidad
                }
                self.carrito_items.append(item)
                self.actualizar_carrito_display()
                
                # Limpiar campos
                self.cantidad_entry.delete(0, tk.END)
                
                messagebox.showinfo("Éxito", f"✅ {producto_seleccionado.nombre} agregado al carrito")
            else:
                disponible = producto_seleccionado.get_cantidad() if producto_seleccionado else 0
                messagebox.showerror("Error", f"⚠️ Stock insuficiente. Disponible: {disponible}")
                
        except ValueError:
            messagebox.showerror("Error", "⚠️ Ingrese una cantidad válida")
        except Exception as e:
            messagebox.showerror("Error", f"⚠️ Error: {str(e)}")

    def registrar_solicitud(self):
        """Abrir ventana para registrar cliente y necesidad (HU14)."""
        from .dialogs import RegisterNeedWindow
        RegisterNeedWindow(self.parent, self.inventario, default_tipo='consulta', allow_tipo_change=False)

    def actualizar_carrito_display(self):
        """Actualizar la visualización del carrito."""
        self.carrito_text.delete(1.0, tk.END)
        
        if not self.carrito_items:
            self.carrito_text.insert(tk.END, "🛒 Carrito vacío\n\nAgregue productos para comenzar la venta.")
            return
            
        total = 0
        texto = f"👤 Cliente: {self.cliente_entry.get()}\n"
        texto += "=" * 50 + "\n"
        
        for i, item in enumerate(self.carrito_items, 1):
            texto += f"{i}. {item['producto'].nombre}\n"
            texto += f"   Cantidad: {item['cantidad']} x ${item['producto'].precio:,} = ${item['subtotal']:,}\n\n"
            total += item['subtotal']
            
        texto += "=" * 50 + "\n"
        texto += f"💰 TOTAL: ${total:,}"
        
        self.carrito_text.insert(tk.END, texto)
        
    def procesar_venta(self):
        """Procesar la venta."""
        if not self.carrito_items:
            messagebox.showerror("Error", "⚠️ El carrito está vacío")
            return
            
        if not self.cliente_entry.get().strip():
            messagebox.showerror("Error", "⚠️ Debe ingresar el nombre del cliente")
            return
        
        try:
            # Calcular total
            total = sum(item['subtotal'] for item in self.carrito_items)
            
            # Confirmar venta
            confirm = messagebox.askyesno("Confirmar Venta",
                                        f"¿Confirmar venta por ${total:,} a {self.cliente_entry.get()}\n"
                                        f"Forma de pago: {self.pago_var.get()}")
            
            if confirm:
                # Copia de los ítems antes de vaciar el carrito
                items_copia = [item.copy() for item in self.carrito_items]

                # Actualizar stock y registrar historial utilizando método del Inventario
                for item in self.carrito_items:
                    producto = item['producto']
                    nueva_cantidad = producto.get_cantidad() - item['cantidad']
                    # Esto registra historial y guarda inventario internamente
                    self.inventario.actualizar_stock(producto.get_codigo(), nueva_cantidad, "ventas")

                # ---------------- Registrar la venta ----------------
                try:
                    from HU.Venta import Venta
                    # Cargar ventas previas (si existe el archivo)
                    Venta.cargar_desde_json()

                    # Construir lista de tuplas (Producto, cantidad)
                    productos_vendidos = [(item['producto'], item['cantidad']) for item in items_copia]

                    # Crear nueva venta
                    nueva_venta = Venta(self.cliente_entry.get(), productos_vendidos, self.pago_var.get())
                    # Guardar actualizaciones en el archivo
                    Venta.guardar_en_json()
                except Exception as e:
                    # No impedir la venta si falla el guardado; solo informar
                    print(f"Error al registrar venta en ventas.json: {e}")

                # Generar comprobante
                self.generar_comprobante_venta(total, items_copia)

                # Mostrar éxito
                messagebox.showinfo("Venta Completada",
                                   f"✅ Venta procesada exitosamente\n"
                                   f"💰 Total: ${total:,}\n"
                                   f"👤 Cliente: {self.cliente_entry.get()}\n"
                                   f"💳 Forma de pago: {self.pago_var.get()}")

                # Limpiar carrito
                self.carrito_items = []
                self.cliente_entry.delete(0, tk.END)
                self.actualizar_carrito_display()

                # Refrescar dashboard si existe
                if self.refresh_callback:
                    self.refresh_callback()

                # Refrescar lista de productos disponibles en ventas
                self._refresh_productos_combo()
                    
        except Exception as e:
            messagebox.showerror("Error", f"⚠️ Error al procesar venta: {str(e)}")

    def generar_comprobante_venta(self, total, items):
        """Generar un comprobante de venta en formato de texto."""
        try:
            os.makedirs("comprobantes", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join("comprobantes", f"comprobante_{timestamp}.txt")

            with open(filename, "w", encoding="utf-8") as f:
                f.write("AGROVET PLUS - COMPROBANTE DE VENTA\n")
                f.write("=" * 50 + "\n")
                f.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"Cliente: {self.cliente_entry.get()}\n")
                f.write(f"Forma de pago: {self.pago_var.get()}\n")
                f.write("-" * 50 + "\n")

                for item in items:
                    nombre = item['producto'].nombre
                    cantidad = item['cantidad']
                    subtotal = item['subtotal']
                    f.write(f"{nombre} x {cantidad} = ${subtotal:,}\n")

                f.write("-" * 50 + "\n")
                f.write(f"TOTAL: ${total:,}\n")
                f.write("=" * 50 + "\n")

            messagebox.showinfo("Comprobante generado", f"🧾 Comprobante guardado en {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"⚠️ Error al generar comprobante: {e}")

    def open_purchase_history(self):
        """Abrir ventana del historial de compras por cliente."""
        from .dialogs import PurchaseHistoryWindow
        PurchaseHistoryWindow(self.parent)

    # --------------------- Utilidades ---------------------
    def _bind_mousewheel(self, widget):
        """Habilitar desplazamiento con la rueda del ratón en el widget suministrado."""
        # Windows y macOS
        widget.bind_all("<MouseWheel>", lambda e: widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        # Linux
        widget.bind_all("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))
        widget.bind_all("<Button-5>", lambda e: widget.yview_scroll(1, "units")) 

    # ------------- Utilidades internas -------------
    def _refresh_productos_combo(self):
        """Actualizar lista de productos en el combobox excluyendo los agotados."""
        productos_disponibles = [p for p in self.inventario.productos if p.get_cantidad() > 0]
        valores = [f"{p.nombre} - ${p.precio:,}" for p in productos_disponibles]
        self.producto_combo['values'] = valores
        # Limpiar selección si producto ya no disponible
        if self.producto_var.get() not in valores:
            self.producto_var.set('')

    # Sobrescribir refresh_callback si se requiere desde afuera
    def external_refresh(self):
        """Método para ser llamado externamente cuando cambie el inventario."""
        self._refresh_productos_combo()
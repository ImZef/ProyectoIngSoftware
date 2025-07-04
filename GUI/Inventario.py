"""
Inventory management component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .configuracion import COLOR_PALETTE, ICONS


class InventoryComponent:
    """Componente para la gestión del inventario."""
    
    def __init__(self, parent, inventario, refresh_callback=None):
        self.parent = parent
        self.inventario = inventario
        self.refresh_callback = refresh_callback
        self.colors = COLOR_PALETTE
        self.products_tree = None
        self.search_entry = None
        self.search_type = None
        
    def create_inventory_tab(self, notebook):
        """Crear la pestaña de inventario."""
        inventory_frame = ttk.Frame(notebook)
        notebook.add(inventory_frame, text=f"{ICONS['inventory']} Inventario")
        
        # Frame superior con controles
        controls_frame = ttk.Frame(inventory_frame)
        controls_frame.pack(fill='x', padx=20, pady=10)
        
        # Búsqueda
        search_frame = ttk.LabelFrame(controls_frame, text=f"{ICONS['search']} Buscar Productos")
        search_frame.pack(fill='x', pady=(0, 10))
        
        search_controls = ttk.Frame(search_frame)
        search_controls.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(search_controls, text="Buscar por:").pack(side='left')
        
        self.search_type = ttk.Combobox(search_controls, values=["Código", "Nombre", "Categoría"], 
                                       state="readonly", width=12)
        self.search_type.pack(side='left', padx=(5, 10))
        self.search_type.set("Nombre")
        
        self.search_entry = ttk.Entry(search_controls, width=30)
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        ttk.Button(search_controls, text=f"{ICONS['search']} Buscar", 
                  command=self.search_products).pack(side='left', padx=(0, 10))
        
        ttk.Button(search_controls, text=f"{ICONS['update']} Mostrar Todos", 
                  command=self.show_all_products).pack(side='left')
        
        # Tabla de productos
        self.create_products_table(inventory_frame)
        
        # Botones de acción
        self.create_inventory_buttons(inventory_frame)
        
        return inventory_frame
        
    def create_products_table(self, parent):
        """Crear la tabla de productos."""
        table_frame = ttk.Frame(parent)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear Treeview
        columns = ('Código', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Estado')
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.products_tree.heading('Código', text='Código')
        self.products_tree.heading('Nombre', text='Nombre')
        self.products_tree.heading('Categoría', text='Categoría')
        self.products_tree.heading('Precio', text='Precio')
        self.products_tree.heading('Stock', text='Stock')
        self.products_tree.heading('Estado', text='Estado')
        
        # Configurar ancho de columnas
        self.products_tree.column('Código', width=80, anchor='center')
        self.products_tree.column('Nombre', width=250)
        self.products_tree.column('Categoría', width=150)
        self.products_tree.column('Precio', width=100, anchor='e')
        self.products_tree.column('Stock', width=80, anchor='center')
        self.products_tree.column('Estado', width=100, anchor='center')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.products_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.products_tree.xview)
        self.products_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar
        self.products_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Cargar productos
        self.load_products_table()
        
    def load_products_table(self, productos=None):
        """Cargar productos en la tabla."""
        # Limpiar tabla
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Usar todos los productos si no se especifica una lista
        if productos is None:
            productos = self.inventario.productos
        
        # Cargar productos
        for producto in productos:
            # Determinar estado
            if producto.get_cantidad() == 0:
                estado = "AGOTADO"
                tags = ('agotado',)
            elif producto.get_cantidad() < 5:
                estado = "STOCK BAJO"
                tags = ('stock_bajo',)
            else:
                estado = "DISPONIBLE"
                tags = ('disponible',)
            
            self.products_tree.insert('', 'end', values=(
                producto.get_codigo(),
                producto.get_nombre(),
                producto.get_categoria(),
                f"${producto.get_precio():,.0f}",
                producto.get_cantidad(),
                estado
            ), tags=tags)
        
        # Configurar colores por estado
        self.products_tree.tag_configure('agotado', background='#ffebee', foreground='#c62828')
        self.products_tree.tag_configure('stock_bajo', background='#fff8e1', foreground='#f57c00')
        self.products_tree.tag_configure('disponible', background='#e8f5e8', foreground='#2e7d32')
    
    def create_inventory_buttons(self, parent):
        """Crear botones de acción del inventario."""
        buttons_frame = ttk.Frame(parent)
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(buttons_frame, text=f"{ICONS['add']} Agregar Producto", 
                  command=self.open_add_product_window,
                  style='Primary.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(buttons_frame, text=f"{ICONS['edit']} Actualizar Stock", 
                  command=self.open_update_stock_window,
                  style='Success.TButton').pack(side='left', padx=(0, 10))
        
        ttk.Button(buttons_frame, text=f"{ICONS['history']} Ver Historial", 
                  command=self.show_stock_history).pack(side='left', padx=(0, 10))
        
        ttk.Button(buttons_frame, text=f"{ICONS['update']} Actualizar", 
                  command=self.refresh_inventory).pack(side='right')
    
    def on_search(self, event=None):
        """Evento de búsqueda en tiempo real."""
        if len(self.search_entry.get()) >= 2:
            self.search_products()
        elif len(self.search_entry.get()) == 0:
            self.show_all_products()
    
    def search_products(self):
        """Buscar productos según criterio."""
        search_term = self.search_entry.get().lower()
        search_type = self.search_type.get()
        
        if not search_term:
            self.show_all_products()
            return
        
        filtered_products = []
        
        for producto in self.inventario.productos:
            if search_type == "Código":
                if search_term in str(producto.get_codigo()):
                    filtered_products.append(producto)
            elif search_type == "Nombre":
                if search_term in producto.get_nombre().lower():
                    filtered_products.append(producto)
            elif search_type == "Categoría":
                if search_term in producto.get_categoria().lower():
                    filtered_products.append(producto)
        
        self.load_products_table(filtered_products)
    
    def show_all_products(self):
        """Mostrar todos los productos."""
        self.search_entry.delete(0, tk.END)
        self.load_products_table()
    
    def refresh_inventory(self):
        """Refrescar inventario."""
        self.inventario.cargar_desde_json()
        self.load_products_table()
        if self.refresh_callback:
            self.refresh_callback()
        messagebox.showinfo("Actualizado", "Inventario actualizado correctamente")
    
    def open_add_product_window(self):
        """Abrir ventana para agregar producto."""
        from .dialogs import AddProductWindow
        AddProductWindow(self.parent, self.inventario, self.refresh_inventory)
    
    def open_update_stock_window(self):
        """Abrir ventana para actualizar stock."""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor seleccione un producto")
            return
        
        item = self.products_tree.item(selected[0])
        codigo = item['values'][0]
        from .dialogs import UpdateStockWindow
        UpdateStockWindow(self.parent, self.inventario, codigo, self.refresh_inventory)
    
    def show_stock_history(self):
        """Mostrar historial de stock."""
        from .dialogs import HistoryWindow
        HistoryWindow(self.parent, self.inventario)

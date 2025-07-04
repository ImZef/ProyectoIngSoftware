"""
Dashboard component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk
from .configuracion import COLOR_PALETTE, ICONS


class DashboardComponent:
    """Componente del dashboard principal con estadísticas y resumen."""
    
    def __init__(self, parent, inventario):
        self.parent = parent
        self.inventario = inventario
        self.colors = COLOR_PALETTE
        
    def create_dashboard_tab(self, notebook, index=None):
        """Crear la pestaña del dashboard."""
        dashboard_frame = ttk.Frame(notebook)
        if index is None:
            notebook.add(dashboard_frame, text=f"{ICONS['dashboard']} Dashboard")
        else:
            notebook.insert(index, dashboard_frame, text=f"{ICONS['dashboard']} Dashboard")
            
        # Configurar layout para que el canvas ocupe todo el espacio
        dashboard_frame.rowconfigure(0, weight=1)
        dashboard_frame.columnconfigure(0, weight=1)
        dashboard_frame.columnconfigure(1, weight=0)

        # Contenedor principal con scroll
        canvas = tk.Canvas(dashboard_frame, bg=self.colors['light_gray'])
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cards de estadísticas
        stats_frame = ttk.Frame(scrollable_frame)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Estadísticas principales
        self.create_stats_cards(stats_frame)
        
        # Productos con stock bajo
        self.create_low_stock_section(scrollable_frame)
        
        # Productos próximos a vencer
        self.create_expiring_products_section(scrollable_frame)
        
        # Ubicar canvas y scrollbar en grid
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        return dashboard_frame
        
    def create_stats_cards(self, parent):
        """Crear las tarjetas de estadísticas."""
        cards_frame = ttk.Frame(parent)
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Calcular estadísticas
        total_productos = len(self.inventario.productos)
        productos_agotados = len([p for p in self.inventario.productos if p.get_cantidad() == 0])
        stock_bajo = len([p for p in self.inventario.productos if 0 < p.get_cantidad() < 5])
        valor_total = sum([p.get_precio() * p.get_cantidad() for p in self.inventario.productos])
        
        # Card 1: Total productos
        self.create_stat_card(cards_frame, "Total Productos", str(total_productos), 
                             "🏪", self.colors['primary'], 0, 0)
        
        # Card 2: Productos agotados
        self.create_stat_card(cards_frame, "Agotados", str(productos_agotados), 
                             ICONS['error'], self.colors['danger'], 0, 1)
        
        # Card 3: Stock bajo
        self.create_stat_card(cards_frame, "Stock Bajo", str(stock_bajo), 
                             ICONS['warning'], self.colors['accent'], 0, 2)
        
        # Card 4: Valor total inventario
        self.create_stat_card(cards_frame, "Valor Total", f"${valor_total:,.0f}", 
                             "💰", self.colors['success'], 0, 3)
        
    def create_stat_card(self, parent, title, value, icon, color, row, col):
        """Crear una tarjeta de estadística individual."""
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
        
        # Configurar padding interno
        card_content = tk.Frame(card_frame, bg=color)
        card_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Icono
        icon_label = tk.Label(card_content, text=icon, font=('Arial', 24), 
                             bg=color, fg=self.colors['white'])
        icon_label.pack()
        
        # Valor
        value_label = tk.Label(card_content, text=value, font=('Arial', 20, 'bold'), 
                              bg=color, fg=self.colors['white'])
        value_label.pack()
        
        # Título
        title_label = tk.Label(card_content, text=title, font=('Arial', 12), 
                              bg=color, fg=self.colors['white'])
        title_label.pack()
        
    def create_low_stock_section(self, parent):
        """Crear sección de productos con stock bajo."""
        low_stock_frame = ttk.LabelFrame(parent, text=f"{ICONS['warning']} Productos con Stock Bajo (< 5 unidades)")
        low_stock_frame.pack(fill='x', padx=20, pady=10)
        
        # Lista de productos con stock bajo
        productos_bajo_stock = [p for p in self.inventario.productos if 0 < p.get_cantidad() < 5]
        
        if productos_bajo_stock:
            for producto in productos_bajo_stock[:5]:  # Mostrar solo los primeros 5
                product_frame = tk.Frame(low_stock_frame, bg=self.colors['white'])
                product_frame.pack(fill='x', padx=10, pady=5)
                
                tk.Label(product_frame, text=f"{ICONS['inventory']} {producto.get_nombre()}", 
                        font=('Arial', 11, 'bold'), bg=self.colors['white']).pack(side='left')
                
                tk.Label(product_frame, text=f"Stock: {producto.get_cantidad()}", 
                        font=('Arial', 10), bg=self.colors['white'], 
                        fg=self.colors['danger']).pack(side='right')
        else:
            tk.Label(low_stock_frame, text=f"{ICONS['success']} Todos los productos tienen stock suficiente", 
                    font=('Arial', 11), bg=self.colors['white'], 
                    fg=self.colors['success']).pack(pady=10)
    
    def create_expiring_products_section(self, parent):
        """Crear sección de productos próximos a vencer."""
        expiring_frame = ttk.LabelFrame(parent, text="📅 Productos Próximos a Vencer")
        expiring_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(expiring_frame, text="🔍 Función de monitoreo de vencimientos disponible próximamente", 
                font=('Arial', 11, 'italic'), bg=self.colors['white'], 
                fg=self.colors['dark_gray']).pack(pady=20)

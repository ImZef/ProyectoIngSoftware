"""
Dashboard component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk
from ..configuracion import COLOR_PALETTE, ICONS


class DashboardComponent:
    """Componente del dashboard principal con estadísticas y resumen."""

    def __init__(self, parent, inventario, rol_usuario=None):
        self.parent = parent
        self.inventario = inventario
        self.rol_usuario = rol_usuario  # Información del rol para mostrar en UI
        self.colors = COLOR_PALETTE
        
    def create_dashboard_tab(self, notebook, index=None):
        """Crear la pestaña del dashboard."""
        # Crear estilo para fondo homogéneo
        style = ttk.Style()
        style.configure('Dashboard.TFrame', background=self.colors['light_gray'])

        dashboard_frame = ttk.Frame(notebook, style='Dashboard.TFrame')
        if index is None:
            notebook.add(dashboard_frame, text=f"{ICONS['dashboard']} Dashboard")
        else:
            notebook.insert(index, dashboard_frame, text=f"{ICONS['dashboard']} Dashboard")
            
        # Encabezado centrado - Similar al diseño de ventas
        header_frame = tk.Frame(dashboard_frame, bg='#f0f0f0', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame,
                              text="📊 Dashboard Principal",
                              font=('Arial', 24, 'bold'),
                              bg='#f0f0f0',
                              fg='#333333')
        title_label.place(relx=0.5, rely=0.5, anchor='center')

        # Frame contenedor para canvas y scrollbar
        content_frame = tk.Frame(dashboard_frame, bg=self.colors['light_gray'])
        content_frame.pack(fill='both', expand=True)

        # Contenedor principal con scroll
        canvas = tk.Canvas(content_frame, bg=self.colors['light_gray'], highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Actualizar área de scroll cuando cambie el contenido
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Crear ventana dentro del canvas y conservar su id para poder ajustarle el ancho
        frame_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Asegurar que el frame interior se expanda siempre al ancho del canvas
        def _resize_inner(event):
            canvas.itemconfigure(frame_window, width=event.width)

        canvas.bind("<Configure>", _resize_inner)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # ---------------- Encabezado con rol ----------------
        if self.rol_usuario:
            role_label = tk.Label(scrollable_frame,
                                  text=f"🔑 Rol actual: {self.rol_usuario['nombre']}",
                                  font=('Arial', 14, 'bold'),
                                  bg=self.colors['light_gray'],
                                  fg=self.colors['dark_gray'])
            role_label.pack(padx=20, pady=(20, 10), anchor='w')

        # Cards de estadísticas
        stats_frame = ttk.Frame(scrollable_frame)
        stats_frame.pack(fill='x', padx=20, pady=20)
        
        # Estadísticas principales
        self.create_stats_cards(stats_frame)
        
        # Productos con stock bajo
        self.create_low_stock_section(scrollable_frame)
        
        # Productos próximos a vencer
        self.create_expiring_products_section(scrollable_frame)
        
        # Empaquetar canvas y scrollbar usando pack
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
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
        from datetime import datetime, timedelta

        expiring_frame = ttk.LabelFrame(parent, text="📅 Productos Próximos a Vencer (≤ 60 días)")
        expiring_frame.pack(fill='x', padx=20, pady=10)

        dias_umbral = 60
        productos_por_vencer = []
        hoy = datetime.now().date()

        for producto in self.inventario.productos:
            try:
                fecha_v = datetime.strptime(producto.get_fecha_vencimiento(), "%d/%m/%Y").date()
                dias_restantes = (fecha_v - hoy).days
                if 0 <= dias_restantes <= dias_umbral:
                    productos_por_vencer.append((producto, dias_restantes))
            except Exception:
                # Si la fecha está mal formateada, ignorar producto
                continue

        # Ordenar por días restantes ascendente
        productos_por_vencer.sort(key=lambda x: x[1])

        if productos_por_vencer:
            for producto, dias in productos_por_vencer[:5]:  # Mostrar primeros 5
                prod_frame = tk.Frame(expiring_frame, bg=self.colors['white'])
                prod_frame.pack(fill='x', padx=10, pady=4)

                tk.Label(prod_frame, text=f"{producto.get_nombre()}", font=('Arial', 11, 'bold'), bg=self.colors['white']).pack(side='left')
                tk.Label(prod_frame, text=f"Vence en {dias} día(s)", font=('Arial', 10), bg=self.colors['white'], fg=self.colors['danger' if dias<=15 else 'accent']).pack(side='right')
        else:
            tk.Label(expiring_frame, text="✅ No hay productos próximos a vencer", font=('Arial', 11), bg=self.colors['white'], fg=self.colors['success']).pack(pady=10)

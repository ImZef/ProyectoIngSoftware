"""
Main application class for AgroVet Plus GUI.
"""

import tkinter as tk
from tkinter import ttk

from HU.HistoriaClinica import HistoriaClinica
from HU.Inventario import Inventario
from .historiaClinica import ClinicalHistoryComponent
from .configuracion import COLOR_PALETTE, FONTS, ICONS
from .dashboard import DashboardComponent
from .Inventario import InventoryComponent


class AgrovetApplication:
    """Aplicación principal de AgroVet Plus."""
    
    def __init__(self, root):
        self.root = root
        self.colors = COLOR_PALETTE
        self.setup_window()
        
        # Inicializar inventario y datos
        self.inventario = Inventario()
        self.inventario.cargar_desde_json()
        HistoriaClinica.cargar_historiales()
        
        # Inicializar componentes ANTES de configurar estilos y crear widgets
        self.dashboard_component = DashboardComponent(self.root, self.inventario)
        self.inventory_component = InventoryComponent(self.root, self.inventario, self.refresh_dashboard)
        self.clinical_component = ClinicalHistoryComponent(self.root)
        
        # Configurar estilos y crear interfaz
        self.setup_styles()
        self.create_widgets()
        
    def setup_window(self):
        """Configurar la ventana principal."""
        self.root.title("Agroveterinaria - Sistema de Gestión")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['primary'])
        self.root.resizable(True, True)
        
        # Centrar la ventana
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        """Configurar estilos de ttk."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos personalizados
        self.style.configure('Title.TLabel', 
                           font=FONTS['title'], 
                           foreground=self.colors['white'],
                           background=self.colors['primary'])
        
        self.style.configure('Subtitle.TLabel', 
                           font=FONTS['subtitle'], 
                           foreground=self.colors['dark_gray'],
                           background=self.colors['light_gray'])
        
        self.style.configure('Card.TFrame', 
                           background=self.colors['white'],
                           relief='raised',
                           borderwidth=2)
        
        self.style.configure('Primary.TButton',
                           font=FONTS['label'],
                           foreground=self.colors['white'],
                           background=self.colors['primary'])
        
        self.style.configure('Success.TButton',
                           font=FONTS['text'],
                           foreground=self.colors['white'],
                           background=self.colors['success'])
        
    def create_widgets(self):
        """Crear los widgets principales."""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Encabezado
        self.create_header(main_frame)
        
        # Contenido principal con pestañas
        self.create_tabs(main_frame)
        
    def create_header(self, parent):
        """Crear el encabezado de la aplicación."""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=80)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Logo y título
        title_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        title_frame.pack(expand=True)
        
        # Icono
        icon_label = tk.Label(title_frame, text=ICONS['vet'], font=('Arial', 32), 
                             bg=self.colors['primary'], fg=self.colors['accent'])
        icon_label.pack(side='left', padx=(0, 20))
        
        # Título principal
        title_label = tk.Label(title_frame, text="Agroveterinaria", 
                              font=FONTS['title'],
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(side='left')
        
        # Subtítulo
        subtitle_label = tk.Label(title_frame, text="Sistema de Gestión ", 
                                 font=FONTS['subtitle'],
                                 bg=self.colors['primary'], fg=self.colors['secondary'])
        subtitle_label.pack(side='left', padx=(20, 0))
        
    def create_tabs(self, parent):
        """Crear el notebook con las pestañas."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)
        
        # Crear pestañas usando componentes
        self.dashboard_component.create_dashboard_tab(self.notebook)
        self.inventory_component.create_inventory_tab(self.notebook)
        self.create_products_tab()
        self.create_history_tab()
        self.clinical_component.create_clinical_history_tab(self.notebook)
        self.create_sales_tab()

    def create_products_tab(self):
        """Crear pestaña de productos (placeholder)."""
        # products_frame = ttk.Frame(self.notebook)
        # self.notebook.add(products_frame, text=f"{ICONS['products']} Productos")
        
        # tk.Label(products_frame, text="Gestión detallada de productos - En desarrollo", 
        #         font=FONTS['header'], bg=self.colors['light_gray']).pack(expand=True)
    
    def create_history_tab(self):
        """Crear pestaña de historial (placeholder)."""
        # history_frame = ttk.Frame(self.notebook)
        # self.notebook.add(history_frame, text=f"{ICONS['history']} Historial")
        
        # tk.Label(history_frame, text="Historial de movimientos y transacciones - En desarrollo", 
        #         font=FONTS['header'], bg=self.colors['light_gray']).pack(expand=True)
    
    def create_sales_tab(self):
        """Crear pestaña de ventas (placeholder)."""
        # sales_frame = ttk.Frame(self.notebook)
        # self.notebook.add(sales_frame, text=f"{ICONS['sales']} Ventas")
        
        # placeholder_frame = tk.Frame(sales_frame, bg=self.colors['light_gray'])
        # placeholder_frame.pack(fill='both', expand=True, padx=20, pady=20)
        # tk.Label(placeholder_frame, text="Gestión de ventas - En desarrollo", 
        #          font=FONTS['header'], bg=self.colors['light_gray']).pack(expand=True)

    def refresh_dashboard(self):
        """Refrescar la pestaña del dashboard."""
        # Buscar índice de la pestaña Dashboard
        dash_index = None
        for idx in range(self.notebook.index("end")):
            if ICONS['dashboard'] in self.notebook.tab(idx, "text"):
                dash_index = idx
                # Remover frame anterior
                self.notebook.forget(idx)
                break
        
        # Recrear pestaña Dashboard en la misma posición
        if dash_index is not None:
            self.dashboard_component.create_dashboard_tab(self.notebook, index=dash_index)


def main():
    """Función principal para ejecutar la aplicación."""
    root = tk.Tk()
    app = AgrovetApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()

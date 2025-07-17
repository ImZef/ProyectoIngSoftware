"""
Main application class for AgroVet Plus GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from HU.HistoriaClinica import HistoriaClinica
from HU.Inventario import Inventario
from .Funcionalidad.historiaClinica import ClinicalHistoryComponent
from .configuracion import COLOR_PALETTE, FONTS, ICONS
from .Funcionalidad.dashboard import DashboardComponent
from .Funcionalidad.Inventario import InventoryComponent
from .Funcionalidad.ventas import SalesComponent
from .roles import role_manager


class AgrovetApplication:
    """Aplicación principal de AgroVet Plus."""
    
    def __init__(self, root, rol_usuario=None):
        self.root = root
        self.rol_usuario = rol_usuario
        self.colors = COLOR_PALETTE
        self.setup_window()
        
        # Inicializar inventario y datos
        self.inventario = Inventario()
        self.inventario.cargar_desde_json()
        # Cargar historiales existentes
        HistoriaClinica.cargar_historiales()
        # Crear muestras si no hay historiales
        if not HistoriaClinica.historiales:
            HistoriaClinica._crear_historiales_muestra()
            HistoriaClinica.guardar_historiales()
        
        # Inicializar componentes ANTES de configurar estilos y crear widgets
        self.dashboard_component = DashboardComponent(self.root, self.inventario, self.rol_usuario)
        self.inventory_component = InventoryComponent(self.root, self.inventario, self.refresh_dashboard)
        self.clinical_component = ClinicalHistoryComponent(self.root)
        from .Funcionalidad.consultas import ConsultasComponent
        self.consultas_component = ConsultasComponent(self.root)
        self.sales_component = SalesComponent(self.root, self.inventario, self.refresh_dashboard)
        # Cuando cambie el inventario, refrescar dashboard y lista de productos en ventas
        self.inventory_component.refresh_callback = self.on_inventory_change
        from .Funcionalidad.pedidos import PedidosComponent
        self.orders_component = PedidosComponent(self.root)
        
        # Configurar estilos y crear interfaz
        self.setup_styles()
        self.create_widgets()
        
    def setup_window(self):
        """Configurar la ventana principal."""
        title_text = "Agroveterinaria - Sistema de Gestión"
        if self.rol_usuario:
            title_text += f" - {self.rol_usuario['nombre']}"
            
        self.root.title(title_text)
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['primary'])
        self.root.resizable(True, True)

        # -------- Pantalla completa --------
        try:
            self.root.state('zoomed')  # Windows
        except Exception:
            self.root.attributes('-fullscreen', True)
        
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
        title_label = tk.Label(title_frame, text="Agroveterinaria Los Caballos", 
                              font=FONTS['title'],
                              bg=self.colors['primary'], fg=self.colors['white'])
        title_label.pack(side='left')
        
        # Subtítulo con rol
        subtitle_text = "Sistema de Gestión"
        if self.rol_usuario:
            subtitle_text += f" - {self.rol_usuario['nombre']}"
            
        subtitle_label = tk.Label(title_frame, text=subtitle_text, 
                                 font=FONTS['subtitle'],
                                 bg=self.colors['primary'], fg=self.colors['secondary'])
        subtitle_label.pack(side='left', padx=(20, 0))

        # Botón Atrás
        back_button = tk.Button(header_frame,
                                text="🔙 Atrás",
                                font=FONTS['label'],
                                bg=self.colors['accent'],
                                fg=self.colors['white'],
                                relief='raised',
                                bd=2,
                                padx=15,
                                pady=5,
                                command=self.go_back)
        back_button.pack(side='right', padx=10)
        
    def create_tabs(self, parent):
        """Crear el notebook con las pestañas."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)
        
        # Crear pestañas basándose en los permisos del rol
        self.create_tabs_based_on_role()

    def create_tabs_based_on_role(self):
        """Crear pestañas basándose en el rol del usuario usando el gestor de roles."""
        if not self.rol_usuario:
            # Si no hay rol definido, mostrar todas las pestañas
            self.create_all_tabs()
            return
        
        # Asegurar que el rol esté establecido en el gestor
        role_manager.set_current_role(self.rol_usuario, 'gui')
        
        # Obtener pestañas accesibles desde el gestor de roles
        accessible_tabs = role_manager.get_accessible_tabs()
        
        # Dashboard siempre visible
        if accessible_tabs['dashboard']:
            self.dashboard_component.create_dashboard_tab(self.notebook)
        
        # Pestañas según permisos
        if accessible_tabs['inventory']:
            self.inventory_component.create_inventory_tab(self.notebook)
            
        if accessible_tabs['clinical_history']:
            self.clinical_component.create_clinical_history_tab(self.notebook)

            # Si el rol es veterinario mostrar pestaña de consultas
            if self.rol_usuario and self.rol_usuario.get('id') == 'veterinario':
                self.consultas_component.create_consultas_tab(self.notebook)
            
        if accessible_tabs['sales']:
            self.sales_component.create_sales_tab(self.notebook)
            
        # Pestaña Citas eliminada

        # Pestaña Productos eliminada
            
        if accessible_tabs['user_management']:
            self.create_user_management_tab()

        if accessible_tabs['orders']:
            self.orders_component.create_pedidos_tab(self.notebook)

    def create_appointments_tab(self):
        """Crear pestaña para agendar citas."""
        appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(appointments_frame, text=f"{ICONS.get('appointments', '📅')} Citas")

        # Contenido principal
        main_frame = tk.Frame(appointments_frame, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        title_label = tk.Label(main_frame,
                               text="📅 Gestión de Citas",
                               font=FONTS['title'],
                               bg=self.colors['light_gray'],
                               fg=self.colors['dark_gray'])
        title_label.pack(pady=(0, 20))

        # Placeholder de funcionalidad
        content_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='raised', bd=2)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        info_label = tk.Label(content_frame,
                              text="📅 Aquí podrá registrar y consultar citas\n\n⚠️ Funcionalidad en desarrollo",
                              font=FONTS['text'],
                              bg=self.colors['white'],
                              fg=self.colors['dark_gray'],
                              justify='left')
        info_label.pack(expand=True, pady=50)

    def create_user_management_tab(self):
        """Crear pestaña de gestión de usuarios (solo Administrador)."""
        users_frame = ttk.Frame(self.notebook)
        self.notebook.add(users_frame, text=f"{ICONS.get('users', '👥')} Usuarios")

        main_frame = tk.Frame(users_frame, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        title_label = tk.Label(main_frame,
                              text="👥 Gestión de Usuarios",
                              font=FONTS['title'],
                              bg=self.colors['light_gray'],
                              fg=self.colors['dark_gray'])
        title_label.pack(pady=(0, 20))

        content_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='raised', bd=2)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        info_label = tk.Label(content_frame,
                              text="🔑 Alta, baja y modificación de cuentas\n\n⚠️ Funcionalidad en desarrollo",
                              font=FONTS['text'],
                              bg=self.colors['white'],
                              fg=self.colors['dark_gray'],
                              justify='left')
        info_label.pack(expand=True, pady=50)

    def create_all_tabs(self):
        """Crear todas las pestañas (modo sin restricciones)."""
        self.dashboard_component.create_dashboard_tab(self.notebook)
        self.inventory_component.create_inventory_tab(self.notebook)
        # self.create_products_tab()  # Eliminada
        # self.create_appointments_tab()  # Eliminada
        self.clinical_component.create_clinical_history_tab(self.notebook)
        self.sales_component.create_sales_tab(self.notebook)
        self.create_user_management_tab()
        self.orders_component.create_pedidos_tab(self.notebook)

    def create_products_tab(self):
        """Crear pestaña de productos."""
        products_frame = ttk.Frame(self.notebook)
        self.notebook.add(products_frame, text=f"{ICONS.get('products', '📦')} Productos")
        
        # Frame principal
        main_frame = tk.Frame(products_frame, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame,
                              text="📦 Gestión de Productos",
                              font=FONTS['title'],
                              bg=self.colors['light_gray'],
                              fg=self.colors['dark_gray'])
        title_label.pack(pady=(0, 20))
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='raised', bd=2)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Información
        info_label = tk.Label(content_frame,
                             text="🔧 Gestión Detallada de Productos\n\n"
                                  "Aquí puede:\n"
                                  "• Ver catálogo completo de productos\n"
                                  "• Editar información de productos\n"
                                  "• Gestionar categorías\n"
                                  "• Analizar tendencias de ventas por producto\n\n"
                                  "⚠️ Funcionalidad en desarrollo",
                             font=FONTS['text'],
                             bg=self.colors['white'],
                             fg=self.colors['dark_gray'],
                             justify='left')
        info_label.pack(expand=True, pady=50)
    
    def create_history_tab(self):
        """Crear pestaña de historial."""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text=f"{ICONS.get('history', '📊')} Historial")
        
        # Frame principal
        main_frame = tk.Frame(history_frame, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame,
                              text="📊 Historial y Reportes",
                              font=FONTS['title'],
                              bg=self.colors['light_gray'],
                              fg=self.colors['dark_gray'])
        title_label.pack(pady=(0, 20))
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='raised', bd=2)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Información
        info_label = tk.Label(content_frame,
                             text="📈 Historial de Movimientos y Reportes\n\n"
                                  "Aquí puede:\n"
                                  "• Ver historial de transacciones\n"
                                  "• Generar reportes de ventas\n"
                                  "• Analizar movimientos de inventario\n"
                                  "• Exportar datos para análisis\n\n"
                                  "⚠️ Funcionalidad en desarrollo",
                             font=FONTS['text'],
                             bg=self.colors['white'],
                             fg=self.colors['dark_gray'],
                             justify='left')
        info_label.pack(expand=True, pady=50)
    
    def refresh_dashboard(self):
        """Reconstruir la pestaña Dashboard para reflejar datos actualizados."""
        if not hasattr(self, 'notebook'):
            return

        try:
            # Pestaña seleccionada en este momento
            selected_tab_before = self.notebook.select()

            dashboard_idx = None
            dashboard_selected = False

            # Ubicar pestaña Dashboard
            for idx, tab_id in enumerate(self.notebook.tabs()):
                if 'Dashboard' in self.notebook.tab(tab_id, 'text'):
                    dashboard_idx = idx
                    dashboard_selected = (tab_id == selected_tab_before)
                    # Eliminar la pestaña actual del dashboard
                    self.notebook.forget(tab_id)
                    break

            # Si existía dashboard, reconstruirlo en la misma posición
            if dashboard_idx is not None:
                self.dashboard_component.create_dashboard_tab(self.notebook, index=dashboard_idx)

                # Recuperar pestaña que estaba activa antes, salvo que fuera el propio dashboard
                if not dashboard_selected:
                    # El usuario estaba en otra pestaña → mantenerla
                    if selected_tab_before in self.notebook.tabs():
                        self.notebook.select(selected_tab_before)
                else:
                    # Si el usuario estaba en dashboard, seleccionar la nueva pestaña creada
                    new_tab_id = self.notebook.tabs()[dashboard_idx]
                    self.notebook.select(new_tab_id)
        except Exception as e:
            print(f"Error al refrescar dashboard: {e}")

    # ---------------- Evento inventario cambió ----------------
    def on_inventory_change(self):
        """Callback global cuando el inventario cambia."""
        # 1) Refrescar el dashboard
        self.refresh_dashboard()
        # 2) Refrescar lista de productos disponibles en ventas
        try:
            self.sales_component._refresh_productos_combo()
        except Exception:
            pass

    def go_back(self):
        """Cerrar la interfaz actual y volver a la selección de rol."""
        try:
            # Cerrar ventana actual
            self.root.destroy()
            # Volver a lanzar la selección de rol
            from .app import main as app_main  # import interno para evitar dependencias circulares
            app_main()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo volver a la selección de rol: {e}")

    # --------------------- Utilidades ---------------------
    def _bind_mousewheel(self, widget):
        """Habilitar desplazamiento con la rueda del ratón en el widget suministrado."""
        # Windows y macOS
        widget.bind_all("<MouseWheel>", lambda e: widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        # Linux
        widget.bind_all("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))
        widget.bind_all("<Button-5>", lambda e: widget.yview_scroll(1, "units"))


def main(rol_usuario=None):
    """Función principal para ejecutar la aplicación."""
    # Si no se pasa un rol desde la consola, mostrar ventana de selección
    from comandos import main as console_main  # Importar aquí para evitar bucles

    if rol_usuario is None:
        resultado = role_manager.select_role_interactively()

        # Si se cierra sin seleccionar nada
        if resultado == (None, None) or resultado is None:
            return

        rol_usuario, interfaz = resultado
        # La autenticación ahora se realiza dentro de la ventana de selección de rol.
    else:
        interfaz = 'gui'
        # Establecer el rol en el gestor para futuras referencias
        if rol_usuario:
            role_manager.set_current_role(rol_usuario, interfaz)

    # Dependiendo de la interfaz seleccionada, lanzar GUI o Consola
    if interfaz == 'gui':
        root = tk.Tk()
        app = AgrovetApplication(root, rol_usuario)
        root.mainloop()
    else:
        console_main(rol_usuario)


if __name__ == "__main__":
    main()

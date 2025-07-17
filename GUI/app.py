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
from HU.GestorUsuarios import GestorUsuarios
import os
# Sólo PNG soportado nativamente por tk.PhotoImage
PIL_AVAILABLE = False


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
        # Gestor de usuarios para administración
        self.user_manager = GestorUsuarios()
        
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
        
        # Logo de Agroveterinaria Los Caballos
        # Buscar logo en varias ubicaciones (.png únicamente)
        search_paths = [
            os.path.join(os.path.dirname(__file__), 'logo.png'),
            os.path.join(os.path.dirname(__file__), '..', 'logo.png')
        ]
        logo_loaded = False
        for lp in search_paths:
            lp = os.path.abspath(lp)
            if os.path.exists(lp):
                try:
                    self.logo_img = tk.PhotoImage(file=lp)
                    logo_label = tk.Label(title_frame, image=self.logo_img, bg=self.colors['primary'])
                    logo_label.pack(side='left', padx=(0, 20))
                    logo_loaded = True
                    break
                except Exception as e:
                    print(f"[Error] al cargar logo.png desde {lp}: {e}")
        if not logo_loaded:
            # No se encontró logo.png; mostrar ícono de texto
            print(f"[Aviso] logo.png no encontrado en: {search_paths}")
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
        # Pestaña de Pedidos para roles con permiso 'pedidos'
        if accessible_tabs.get('orders'):
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


    def create_user_management_tab(self):
        # Pestaña de Gestión de Usuarios para administradores
        users_frame = ttk.Frame(self.notebook)
        self.notebook.add(users_frame, text=f"{ICONS.get('users','👥')} Usuarios")
        main_frame = tk.Frame(users_frame, bg=self.colors['light_gray'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        # Título
        title_label = tk.Label(main_frame, text="👥 Gestión de Usuarios", font=FONTS['title'],
                              bg=self.colors['light_gray'], fg=self.colors['dark_gray'])
        title_label.pack(pady=(0, 20))
        # Contenedor principal
        content_frame = tk.Frame(main_frame, bg=self.colors['white'], relief='raised', bd=2)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        # Formulario para agregar nuevo usuario
        form_frame = tk.LabelFrame(content_frame, text="➕ Nuevo Usuario", font=FONTS['subtitle'],
                                  bg=self.colors['white'], fg=self.colors['dark_gray'], padx=10, pady=10)
        form_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(form_frame, text="Username:", font=FONTS['label'], bg=self.colors['white']).grid(row=0, column=0, pady=5, sticky='e')
        self.username_entry = tk.Entry(form_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=5)
        tk.Label(form_frame, text="Nombre:", font=FONTS['label'], bg=self.colors['white']).grid(row=1, column=0, pady=5, sticky='e')
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)
        tk.Label(form_frame, text="Rol:", font=FONTS['label'], bg=self.colors['white']).grid(row=2, column=0, pady=5, sticky='e')
        roles = role_manager.get_available_roles()
        # Orden descendente: primero IDs numéricos, luego alfanuméricos
        numeric = [(rid, info) for rid, info in roles.items() if rid.isdigit()]
        alpha = [(rid, info) for rid, info in roles.items() if not rid.isdigit()]
        numeric_sorted = sorted(numeric, key=lambda kv: int(kv[0]), reverse=True)
        alpha_sorted = sorted(alpha, key=lambda kv: kv[0], reverse=True)
        sorted_roles = numeric_sorted + alpha_sorted
        role_options = [f"{rid}: {info['nombre']}" for rid, info in sorted_roles]
        self.new_role_var = tk.StringVar()
        self.new_role_combo = ttk.Combobox(form_frame, textvariable=self.new_role_var, values=role_options,
                                           state='readonly', width=28)
        self.new_role_combo.grid(row=2, column=1, pady=5, padx=5)
        tk.Button(form_frame, text="Agregar Usuario", bg=self.colors['success'], fg=self.colors['white'],
                  command=self._add_user).grid(row=3, column=0, columnspan=2, pady=10)
        # Tabla de usuarios existentes
        table_frame = tk.LabelFrame(content_frame, text="📋 Usuarios Existentes", font=FONTS['subtitle'],
                                    bg=self.colors['white'], fg=self.colors['dark_gray'], padx=10, pady=10)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        cols = ('Username', 'Nombre', 'Rol')
        self.users_tree = ttk.Treeview(table_frame, columns=cols, show='headings')
        for c in cols:
            self.users_tree.heading(c, text=c)
            self.users_tree.column(c, anchor='center')
        self.users_tree.pack(fill='both', expand=True)
        # Controles para cambio de rol
        control_frame = tk.Frame(content_frame, bg=self.colors['white'])
        control_frame.pack(fill='x', padx=10, pady=(0,10))
        tk.Label(control_frame, text="Nuevo Rol:", font=FONTS['label'], bg=self.colors['white']).pack(side='left')
        self.update_role_var = tk.StringVar()
        self.update_role_combo = ttk.Combobox(control_frame, textvariable=self.update_role_var,
                                             values=role_options, state='readonly', width=25)
        self.update_role_combo.pack(side='left', padx=5)
        tk.Button(control_frame, text="Actualizar Rol", bg=self.colors['accent'], fg=self.colors['white'],
                   command=self._update_user_role).pack(side='left', padx=5)
        # Botones de editar y eliminar usuario seleccionado
        tk.Button(control_frame, text="✏️ Editar Nombre", bg=self.colors['primary'], fg=self.colors['white'],
                  command=self._edit_user).pack(side='left', padx=5)
        tk.Button(control_frame, text="🗑️ Eliminar Usuario", bg=self.colors['danger'], fg=self.colors['white'],
                  command=self._delete_user).pack(side='left', padx=5)
        # Inicializar lista
        self._refresh_users_table()

    def _add_user(self):
        """Agregar un nuevo usuario con los datos del formulario."""
        username = self.username_entry.get().strip()
        nombre = self.name_entry.get().strip()
        rol_seleccionado = self.new_role_var.get()

        if not username or not nombre or not rol_seleccionado:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            # Obtener ID de rol seleccionado
            rol_id = rol_seleccionado.split(':')[0]

            # Crear nuevo usuario
            self.user_manager.agregar_usuario(username, nombre, rol_id)

            # Limpiar formulario
            self.username_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.new_role_var.set('')

            # Actualizar tabla de usuarios
            self._refresh_users_table()

            messagebox.showinfo("Éxito", "Usuario agregado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el usuario: {e}")

    def _refresh_users_table(self):
        """Actualizar la tabla de usuarios existentes."""
        try:
            # Limpiar tabla
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            # Obtener usuarios desde el gestor
            usuarios = self.user_manager.listar_usuarios()
            # Insertar en la tabla (lista de objetos Usuario)
            for user in usuarios:
                self.users_tree.insert('', 'end', values=(user.username, user.nombre, user.rol_id))

            # Ajustar ancho de columnas
            for col in self.users_tree['columns']:
                self.users_tree.column(col, width=max(100, self.users_tree.column(col, 'width')))
        except Exception as e:
            print(f"Error al refrescar tabla de usuarios: {e}")

    def _update_user_role(self):
        """Actualizar el rol del usuario seleccionado en la tabla."""
        try:
            # Obtener usuario seleccionado
            selected_item = self.users_tree.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un usuario de la tabla.")
                return

            # Obtener nuevo rol
            nuevo_rol_seleccionado = self.update_role_var.get()
            if not nuevo_rol_seleccionado:
                messagebox.showwarning("Advertencia", "Seleccione un nuevo rol.")
                return

            nuevo_rol_id = nuevo_rol_seleccionado.split(':')[0]

            # Actualizar rol del usuario
            for item in selected_item:
                username = self.users_tree.item(item, 'values')[0]
                self.user_manager.actualizar_rol(username, nuevo_rol_id)

            messagebox.showinfo("Éxito", "Rol de usuario actualizado exitosamente.")
            self._refresh_users_table()  # Refrescar tabla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el rol del usuario: {e}")

    def _edit_user(self):
        """Editar el nombre del usuario seleccionado."""
        try:
            # Obtener usuario seleccionado
            selected_item = self.users_tree.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un usuario de la tabla.")
                return

            # Obtener nombre actual
            username = self.users_tree.item(selected_item, 'values')[0]

            # Pedir nuevo nombre
            nuevo_nombre = simpledialog.askstring("Editar Nombre", "Ingrese el nuevo nombre:", parent=self.root)
            if not nuevo_nombre:
                return  # Cancelado o vacío

            # Actualizar nombre de usuario
            self.user_manager.editar_nombre(username, nuevo_nombre)

            messagebox.showinfo("Éxito", "Nombre de usuario actualizado exitosamente.")
            self._refresh_users_table()  # Refrescar tabla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar el usuario: {e}")

    def _delete_user(self):
        """Eliminar el usuario seleccionado."""
        try:
            # Obtener usuario seleccionado
            selected_item = self.users_tree.selection()
            if not selected_item:
                messagebox.showwarning("Advertencia", "Seleccione un usuario de la tabla.")
                return

            # Confirmar eliminación
            confirm = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar el usuario seleccionado?", parent=self.root)
            if not confirm:
                return

            # Eliminar usuario
            for item in selected_item:
                username = self.users_tree.item(item, 'values')[0]
                self.user_manager.eliminar_usuario(username)

            messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
            self._refresh_users_table()  # Refrescar tabla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")


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

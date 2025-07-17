"""
Role selection window component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from ..configuracion import COLOR_PALETTE, FONTS
from . import AVAILABLE_ROLES as ROLES_DISPONIBLES


# --- Credenciales por rol ---
CREDENTIALS = {
    '4': ('admin', 'admin123'),            # Administrador
    '1': ('auxventas', 'auxventas123'),    # Auxiliar de Ventas
    '2': ('bod', 'bodeguero123'),          # Bodeguero
    'veterinario': ('vet', 'veterinario123')
}


class RoleSelectionWindow:
    """Ventana de selección de roles gráfica."""
    
    def __init__(self):
        self.selected_role = None
        self.selected_interface = 'gui'
        self.window = tk.Tk()
        self.window.title("AgroVet Plus - Selección de Rol")
        self.window.geometry("800x650")
        self.window.resizable(True, True)

        # ------- Pantalla completa -------
        try:
            # Windows suele soportar 'zoomed'
            self.window.state('zoomed')
        except Exception:
            # Fallback multiplataforma
            self.window.attributes('-fullscreen', True)
        
        # Centrar ventana
        self.center_window()
        
        # Configurar colores
        self.colors = COLOR_PALETTE
        self.window.configure(bg=self.colors['primary'])
        
        self.role_buttons = {}  # Referencia a botones de rol
        self.confirmed = False  # Marca si el usuario confirmó la selección
        self.create_widgets()
        
    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.window.update_idletasks()
        width = 700
        height = 550
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Crear los widgets de la ventana."""
        # Frame principal
        main_frame = tk.Frame(self.window, bg=self.colors['primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(main_frame, 
                              text="👤 SELECCIÓN DE ROL",
                              font=FONTS['title'],
                              bg=self.colors['primary'],
                              fg=self.colors['white'])
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame,
                                 text="Seleccione su rol en el sistema:",
                                 font=FONTS['subtitle'],
                                 bg=self.colors['primary'],
                                 fg=self.colors['secondary'])
        subtitle_label.pack(pady=(0, 20))
        
        # ------------ Selección de tipo de interfaz -------------
        interface_label = tk.Label(main_frame,
                                   text="Seleccione el tipo de interfaz:",
                                   font=FONTS['subtitle'],
                                   bg=self.colors['primary'],
                                   fg=self.colors['secondary'])
        interface_label.pack(pady=(10, 5))

        interface_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        interface_frame.pack(pady=(0, 20))

        self.interface_var = tk.StringVar(value='gui')

        gui_radio = tk.Radiobutton(interface_frame,
                                   text="🖥️ Gráfica (Tkinter)",
                                   variable=self.interface_var,
                                   value='gui',
                                   font=FONTS['label'],
                                   bg=self.colors['primary'],
                                   fg=self.colors['white'],
                                   selectcolor=self.colors['accent'],
                                   activebackground=self.colors['primary'])
        gui_radio.pack(side='left', padx=10)

        console_radio = tk.Radiobutton(interface_frame,
                                       text="💻 Consola",
                                       variable=self.interface_var,
                                       value='console',
                                       font=FONTS['label'],
                                       bg=self.colors['primary'],
                                       fg=self.colors['white'],
                                       selectcolor=self.colors['accent'],
                                       activebackground=self.colors['primary'])
        console_radio.pack(side='left', padx=10)

        # ------------ Selección de Rol -------------------------
        # --------------- Contenedor scrollable de roles ---------------
        roles_container_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        roles_container_frame.pack(fill='both', expand=True, pady=10)

        canvas = tk.Canvas(roles_container_frame, bg=self.colors['primary'], highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(roles_container_frame, orient='vertical', command=canvas.yview)
        roles_frame = tk.Frame(canvas, bg=self.colors['primary'])

        roles_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Anclar grid al centro para que los botones queden centrados
        roles_frame.grid_anchor('center')

        canvas.create_window((0, 0), window=roles_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # --- Enlazar el scroll de la rueda del ratón ---
        self._bind_mousewheel(canvas)

        # Crear botones para cada rol
        for idx, (key, rol) in enumerate(ROLES_DISPONIBLES.items()):
            self.create_role_button(roles_frame, key, rol, column=idx)

        # ------------------ Sección de autenticación ------------------
        auth_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        auth_frame.pack(fill='x', pady=(10, 10))

        auth_title = tk.Label(auth_frame,
                              text="🔐 Credenciales",
                              font=FONTS['subtitle'],
                              bg=self.colors['primary'],
                              fg=self.colors['secondary'])
        auth_title.pack(anchor='w')

        user_label = tk.Label(auth_frame, text="Usuario:", font=FONTS['label'], bg=self.colors['primary'], fg=self.colors['white'])
        user_label.pack(anchor='w', padx=(0, 5))
        self.username_entry = tk.Entry(auth_frame, state='disabled')
        self.username_entry.pack(fill='x', pady=5)

        pwd_label = tk.Label(auth_frame, text="Contraseña:", font=FONTS['label'], bg=self.colors['primary'], fg=self.colors['white'])
        pwd_label.pack(anchor='w', padx=(0, 5))

        pwd_frame = tk.Frame(auth_frame, bg=self.colors['primary'])
        pwd_frame.pack(fill='x', padx=20, pady=(0,10))

        self.password_entry = tk.Entry(pwd_frame, show='*', state='disabled')
        self.password_entry.pack(side='left', fill='x', expand=True)

        # Checkbox mostrar contraseña
        self.show_pwd_var = tk.BooleanVar(value=False)
        show_chk = tk.Checkbutton(pwd_frame, text='👁', variable=self.show_pwd_var,
                                  command=self._toggle_password, bg=self.colors['primary'], fg=self.colors['white'],
                                  activebackground=self.colors['primary'], selectcolor=self.colors['primary'])
        show_chk.pack(side='left', padx=(5,0))

        # Bind Enter para confirmar
        self.password_entry.bind('<Return>', lambda e: self.confirm_selection())

        # Botón confirmar (habilitado tras seleccionar un rol)
        self.confirm_button = tk.Button(roles_frame,
                                        text="✔️ Confirmar",
                                        font=FONTS['label'],
                                        bg=self.colors['dark_gray'],
                                        fg=self.colors['white'],
                                        relief='raised',
                                        bd=2,
                                        padx=20,
                                        pady=10,
                                        state='disabled',
                                        command=self.confirm_selection)
        total_cols = len(ROLES_DISPONIBLES)
        self.confirm_button.grid(row=1, column=0, columnspan=total_cols, sticky='ew', pady=10)

        # Botón de salir
        exit_button = tk.Button(roles_frame,
                               text="❌ Salir",
                               font=FONTS['label'],
                               bg=self.colors['danger'],
                               fg=self.colors['white'],
                               relief='raised',
                               bd=2,
                               padx=20,
                               pady=10,
                               command=self.exit_application)
        exit_button.grid(row=2, column=0, columnspan=total_cols, sticky='ew', pady=5)

        # Variable para animación
        self._anim_flag = False  # Animación activa
        self._after_id = None    # Identificador de la llamada after
        
    def create_role_button(self, parent, key, rol, column=0):
        """Crear un botón para un rol específico."""
        # Frame para el rol
        # Asegurar que columnas se expandan y permitan centrado
        parent.grid_columnconfigure(column, weight=1)
        parent.grid_rowconfigure(0, weight=1)

        role_frame = tk.Frame(parent, bg=self.colors['white'], relief='raised', bd=2)
        role_frame.grid(row=0, column=column, padx=5, pady=5, sticky='n')
        
        # Botón principal del rol
        role_button = tk.Button(role_frame,
                               text=f"👥 {rol['nombre']}",
                               font=FONTS['label'],
                               bg=self.colors['accent'],
                               fg=self.colors['white'],
                               relief='flat',
                               padx=20,
                               pady=15,
                               command=lambda: self.select_role(key))
        role_button.pack(fill='both', expand=True)

        # Guardar referencia para poder resaltar selección
        self.role_buttons[key] = role_button
        
        # Etiqueta con permisos
        permisos_text = f"🔑 Permisos: {', '.join(rol['permisos'][:2])}{'...' if len(rol['permisos']) > 2 else ''}"
        permisos_label = tk.Label(role_frame,
                                 text=permisos_text,
                                 font=FONTS['text'],
                                 bg=self.colors['white'],
                                 fg=self.colors['dark_gray'],
                                 pady=5)
        permisos_label.pack()
        
    def select_role(self, role_key):
        """Seleccionar un rol y actualizar el botón de confirmar."""
        self.selected_role = ROLES_DISPONIBLES[role_key]

        # Resaltar botón seleccionado y restablecer otros
        for k, btn in self.role_buttons.items():
            if k == role_key:
                btn.config(bg=self.colors['success'])
            else:
                btn.config(bg=self.colors['accent'])

        # Habilitar campos de autenticación
        self.username_entry.config(state='normal')
        self.password_entry.config(state='normal')
        # Autocompletar usuario sugerido y limpiar password
        role_id = str(self.selected_role.get('id'))
        suggested = CREDENTIALS.get(role_id, ('', ''))[0]
        self.username_entry.delete(0, 'end')
        self.username_entry.insert(0, suggested)

        self.password_entry.delete(0, 'end')
        self.username_entry.focus_set()

        if not self.confirm_button.winfo_ismapped():
            total_cols = len(ROLES_DISPONIBLES)
            self.confirm_button.grid(row=1, column=0, columnspan=total_cols, sticky='ew', pady=10)
        self.confirm_button.config(state='normal', bg=self.colors['success'])
        self.start_confirm_animation()

    def _toggle_password(self):
        if self.show_pwd_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')
        
    def confirm_selection(self):
        """Validar credenciales y confirmar la selección."""
        # Obtener interfaz seleccionada
        self.selected_interface = self.interface_var.get()

        # Si el rol no requiere credenciales, aceptar directamente
        role_id = str(self.selected_role.get('id')) if self.selected_role else None
        expected = CREDENTIALS.get(role_id)
        if expected:
            user = self.username_entry.get().strip()
            pwd = self.password_entry.get().strip()
            if (user, pwd) != expected:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
                return  # Mantener ventana abierta para reintentar
        # Credenciales correctas (o no requeridas)
        self.confirmed = True
        self.stop_confirm_animation()
        self.window.quit()
        self.window.destroy()
        
    def exit_application(self):
        """Salir de la aplicación."""
        self.confirmed = False
        self.stop_confirm_animation()
        self.window.quit()
        self.window.destroy()
        
    def show(self):
        """Mostrar la ventana y retornar el rol seleccionado."""
        self.window.mainloop()
        if self.confirmed:
            return self.selected_role, self.selected_interface
        else:
            return None, None

    # ---------------- Animación botón confirmar ---------------
    def start_confirm_animation(self):
        if self._anim_flag:
            return
        self._anim_flag = True
        # Iniciar la primera llamada y guardar su id
        self._after_id = self.window.after(600, self._animate_confirm)

    def _animate_confirm(self):
        """Animar el botón 'Confirmar' cambiando su color cada 600 ms."""
        if not self._anim_flag or not self.window.winfo_exists():
            return
        current_color = self.confirm_button.cget('bg')
        new_color = self.colors['accent'] if current_color == self.colors['success'] else self.colors['success']
        self.confirm_button.config(bg=new_color)
        # Programar la siguiente iteración y actualizar el id
        self._after_id = self.window.after(600, self._animate_confirm)

    def stop_confirm_animation(self):
        """Detener la animación y restaurar el color del botón."""
        self._anim_flag = False
        if self._after_id is not None:
            try:
                self.window.after_cancel(self._after_id)
            except Exception:
                pass  # Puede que ya esté cancelado o la ventana cerrada
            self._after_id = None
        self.confirm_button.config(bg=self.colors['success'] if self.confirm_button['state'] == 'normal' else self.colors['dark_gray'])

    def _bind_mousewheel(self, widget):
        """Habilitar desplazamiento con la rueda del ratón (multi-plataforma)."""
        # Windows y MacOS
        widget.bind_all("<MouseWheel>", lambda e: widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        # Linux (rueda arriba/abajo)
        widget.bind_all("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))
        widget.bind_all("<Button-5>", lambda e: widget.yview_scroll(1, "units"))


def create_role_selection_window():
    """Función de utilidad para crear y mostrar la ventana de selección de roles."""
    role_window = RoleSelectionWindow()
    return role_window.show() 
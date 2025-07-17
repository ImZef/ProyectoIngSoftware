"""
Role selection window component for AgroVet Plus application.
"""

import tkinter as tk
from tkinter import ttk, messagebox

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
        self.confirmed = False
        self._anim_flag = False
        self._after_id = None

        self.window = tk.Tk()
        self.window.title("AgroVet Plus - Selección de Rol")
        self.window.geometry("800x650")
        self.window.resizable(True, True)
        try:
            self.window.state('zoomed')
        except Exception:
            self.window.attributes('-fullscreen', True)
        self.center_window()
        self.colors = COLOR_PALETTE
        self.window.configure(bg=self.colors['primary'])

        self.role_buttons = {}
        self.create_widgets()

    def center_window(self):
        """Centrar la ventana en la pantalla."""
        self.window.update_idletasks()
        width = 700
        height = 550
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        """Crear los widgets de la ventana."""
        main_frame = tk.Frame(self.window, bg=self.colors['primary'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Título
        tk.Label(main_frame, text="👤 SELECCIÓN DE ROL", font=FONTS['title'],
                 bg=self.colors['primary'], fg=self.colors['white']).pack(pady=(0,10))
        tk.Label(main_frame, text="Seleccione su rol en el sistema:", font=FONTS['subtitle'],
                 bg=self.colors['primary'], fg=self.colors['secondary']).pack(pady=(0,20))

        # Interfaz fija en Tkinter
        tk.Label(main_frame, text="Interfaz diseñada en Tkinter", font=FONTS['subtitle'],
                 bg=self.colors['primary'], fg=self.colors['secondary']).pack(pady=(0,20))

        # Roles scrollable
        roles_container = tk.Frame(main_frame, bg=self.colors['primary'])
        roles_container.pack(fill='both', expand=True, pady=10)
        canvas = tk.Canvas(roles_container, bg=self.colors['primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(roles_container, orient='vertical', command=canvas.yview)
        roles_frame = tk.Frame(canvas, bg=self.colors['primary'])
        # Ajustar scrollregion al contenido de roles_frame
        roles_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        # Grid interno centrado: distribuir columnas uniformemente
        roles_frame.grid_anchor('center')
        # Crear ventana de roles y anclar al noroeste
        window_id = canvas.create_window((0,0), window=roles_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        # Ajustar roles_frame ancho al canvas para distribución simétrica
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(window_id, width=e.width))
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self._bind_mousewheel(canvas)

        # Create role buttons
        for idx, (key, rol) in enumerate(ROLES_DISPONIBLES.items()):
            self.create_role_button(roles_frame, key, rol, idx)

        # Auth frame (hidden)
        self.auth_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        tk.Label(self.auth_frame, text="🔐 Credenciales", font=FONTS['header'],
                 bg=self.colors['primary'], fg=self.colors['secondary']).pack(pady=(0,10), anchor='center')
        tk.Label(self.auth_frame, text="Usuario:", font=FONTS['subtitle'],
                 bg=self.colors['primary'], fg=self.colors['white']).pack(anchor='center')
        self.username_entry = tk.Entry(self.auth_frame, state='disabled', font=FONTS['subtitle'], justify='center', width=40)
        self.username_entry.pack(pady=5)
        tk.Label(self.auth_frame, text="Contraseña:", font=FONTS['subtitle'],
                 bg=self.colors['primary'], fg=self.colors['white']).pack(anchor='center')
        pwd_frame = tk.Frame(self.auth_frame, bg=self.colors['primary'])
        pwd_frame.pack(pady=(0,10))
        self.password_entry = tk.Entry(pwd_frame, show='*', state='disabled', font=FONTS['subtitle'], justify='center', width=40)
        self.password_entry.pack()
        self.show_pwd_var = tk.BooleanVar(value=False)
        tk.Checkbutton(pwd_frame, text='👁', variable=self.show_pwd_var,
                       command=self._toggle_password, bg=self.colors['primary'], fg=self.colors['white'],
                       activebackground=self.colors['primary'], selectcolor=self.colors['primary']).pack(side='left')
        self.password_entry.bind('<Return>', lambda e: self.confirm_selection())
        self.auth_frame.pack_forget()

        # Action frame (hidden)
        self.action_frame = tk.Frame(main_frame, bg=self.colors['primary'])
        self.confirm_button = tk.Button(self.action_frame, text="✔️ Confirmar", font=FONTS['header'],
                                        fg=self.colors['white'], bg=self.colors['success'], relief='raised', bd=2,
                                        padx=20, pady=10, state='disabled', command=self.confirm_selection)
        self.confirm_button.pack(side='left', fill='x', expand=True, padx=10)
        self.exit_button = tk.Button(self.action_frame, text="❌ Salir", font=FONTS['label'],
                                     fg=self.colors['white'], bg=self.colors['danger'], relief='raised', bd=2,
                                     padx=20, pady=10, command=self.exit_application)
        self.exit_button.pack(side='left', fill='x', expand=True, padx=10)
        self.action_frame.pack_forget()

    def create_role_button(self, parent, key, rol, column):
        """Crear un botón de rol."""
        frame = tk.Frame(parent, bg=self.colors['white'], bd=1, relief='solid')
        frame.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        btn = tk.Button(frame, text=rol.get('nombre',''), font=FONTS['label'],
                        bg=self.colors['accent'], fg=self.colors['white'],
                        command=lambda k=key: self.select_role(k))
        btn.pack(fill='both', expand=True)
        self.role_buttons[key] = btn
        # permisos label
        permisos = rol.get('permisos', [])
        txt = f"🔑 Permisos: {', '.join(permisos[:2])}{'...' if len(permisos)>2 else ''}"
        tk.Label(frame, text=txt, font=FONTS['text'], bg=self.colors['white'], fg=self.colors['dark_gray']).pack(pady=5)

    def select_role(self, role_key):
        """Seleccionar un rol, habilitar autenticación y mostrar botones."""
        self.selected_role = ROLES_DISPONIBLES[role_key]
        # highlight
        for k, b in self.role_buttons.items():
            b.config(bg=self.colors['success'] if k==role_key else self.colors['accent'])
        # enable fields
        self.username_entry.config(state='normal')
        self.password_entry.config(state='normal')
        # suggest username
        role_id = str(self.selected_role.get('id'))
        sugg = CREDENTIALS.get(role_id, ('',''))[0]
        self.username_entry.delete(0,'end')
        self.username_entry.insert(0, sugg)
        self.password_entry.delete(0,'end')
        self.username_entry.focus_set()
        # show auth and action frames centered
        # Mostrar auth y action centrados
        self.auth_frame.pack(pady=(20,5), anchor='center')
        self.action_frame.pack(pady=(5,15), anchor='center')
        self.confirm_button.config(state='normal')
        self.start_confirm_animation()

    def _toggle_password(self):
        show = '' if self.show_pwd_var.get() else '*'
        self.password_entry.config(show=show)

    def confirm_selection(self):
        """Validar credenciales y cerrar si correctas."""
        # Interfaz fija en Tkinter
        self.selected_interface = 'gui'
        role_id = str(self.selected_role.get('id')) if self.selected_role else None
        expected = CREDENTIALS.get(role_id)
        if expected:
            user = self.username_entry.get().strip()
            pwd = self.password_entry.get().strip()
            if (user,pwd)!=expected:
                messagebox.showerror("Error","Usuario o contraseña incorrectos.")
                return
        self.confirmed = True
        self.stop_confirm_animation()
        self.window.quit()
        self.window.destroy()

    def exit_application(self):
        """Salir sin confirmar."""
        self.confirmed = False
        self.stop_confirm_animation()
        self.window.quit()
        self.window.destroy()

    def show(self):
        """Mostrar ventana y devolver selección."""
        self.window.mainloop()
        if self.confirmed:
            return self.selected_role, self.selected_interface
        return None, None

    def start_confirm_animation(self):
        if self._anim_flag: return
        self._anim_flag = True
        self._after_id = self.window.after(600, self._animate_confirm)

    def _animate_confirm(self):
        if not self._anim_flag or not self.window.winfo_exists(): return
        curr = self.confirm_button.cget('bg')
        new = self.colors['accent'] if curr==self.colors['success'] else self.colors['success']
        self.confirm_button.config(bg=new)
        self._after_id = self.window.after(600, self._animate_confirm)

    def stop_confirm_animation(self):
        if not self._anim_flag: return
        self._anim_flag = False
        if self._after_id:
            try: self.window.after_cancel(self._after_id)
            except: pass
            self._after_id = None
        self.confirm_button.config(bg=self.colors['success'] if self.confirm_button['state']=='normal' else self.colors['dark_gray'])

    def _bind_mousewheel(self, widget):
        widget.bind_all("<MouseWheel>", lambda e: widget.yview_scroll(int(-1*(e.delta/120)), 'units'))
        widget.bind_all("<Button-4>", lambda e: widget.yview_scroll(-1,'units'))
        widget.bind_all("<Button-5>", lambda e: widget.yview_scroll(1,'units'))


def create_role_selection_window():
    """Función para crear y mostrar la ventana de selección de roles."""
    window = RoleSelectionWindow()
    return window.show()
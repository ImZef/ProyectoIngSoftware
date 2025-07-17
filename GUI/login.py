import tkinter as tk
from tkinter import Tk, Toplevel, messagebox
from tkinter import ttk
from .configuracion import COLOR_PALETTE, FONTS, ICONS, WINDOW_CONFIG

CREDENTIALS = {
    # id_rol: (usuario, contraseña)
    '4': ('admin', 'admin123'),        # Administrador
    '1': ('auxventas', 'auxventas123'),# Auxiliar de Ventas
    '2': ('bod', 'bodeguero123'),      # Bodeguero
    'veterinario': ('vet', 'veterinario123')
}

def _center_window(win, width=350, height=220):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def prompt_login(role_info):
    """Muestra una ventana de inicio de sesión.

    Parámetros
    ----------
    role_info : dict
        Diccionario ROLE_INFO del rol seleccionado.

    Retorna
    -------
    bool
        True si la autenticación es correcta, False en caso contrario (o cierre).
    """
    role_id = str(role_info.get('id'))
    creds = CREDENTIALS.get(role_id)
    if not creds:
        # Si no hay credenciales para el rol, permitir acceso directo
        return True

    root = Tk()
    root.withdraw()  # Ocultar ventana principal

    dialog = Toplevel()
    # Estilizar ventana
    dialog.configure(bg=COLOR_PALETTE['primary'])
    dialog.title("Inicio de Sesión")
    _center_window(dialog, 350, 220)
    dialog.resizable(False, False)

    tk.Label(dialog, text=f"🔐 Autenticación - {role_info.get('nombre', '')}",
             font=FONTS['header'], bg=COLOR_PALETTE['primary'], fg=COLOR_PALETTE['white']
             ).pack(pady=(10, 20))

    tk.Label(dialog, text="Usuario:", font=FONTS['label'],
             bg=COLOR_PALETTE['primary'], fg=COLOR_PALETTE['white']
             ).pack(anchor='w', padx=20)
    username_entry = tk.Entry(dialog, font=FONTS['text'])
    username_entry.pack(fill='x', padx=20, pady=5)

    tk.Label(dialog, text="Contraseña:", font=FONTS['label'],
             bg=COLOR_PALETTE['primary'], fg=COLOR_PALETTE['white']
             ).pack(anchor='w', padx=20)
    password_entry = tk.Entry(dialog, show='*', font=FONTS['text'])
    password_entry.pack(fill='x', padx=20, pady=5)

    result = {'success': False}

    def on_accept():
        user = username_entry.get().strip()
        pwd = password_entry.get().strip()
        if (user, pwd) == creds:
            result['success'] = True
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            username_entry.focus_set()

    def on_cancel():
        dialog.destroy()

    # Mostrar/ocultar contraseña
    show_pwd_var = tk.BooleanVar(value=False)
    def _toggle_password():
        password_entry.config(show='' if show_pwd_var.get() else '*')
    tk.Checkbutton(dialog, text="Mostrar contraseña", variable=show_pwd_var,
                   command=_toggle_password, bg=COLOR_PALETTE['primary'],
                   fg=COLOR_PALETTE['white'], font=FONTS['label']
                   ).pack(anchor='w', padx=20, pady=(0,10))

    # Botones de acción
    btn_frame = tk.Frame(dialog, bg=COLOR_PALETTE['primary'])
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Ingresar", command=on_accept,
              bg=COLOR_PALETTE['accent'], fg=COLOR_PALETTE['white'],
              font=FONTS['label'], width=12, bd=0
              ).pack(side='left', padx=10)
    tk.Button(btn_frame, text="Cancelar", command=on_cancel,
              bg=COLOR_PALETTE['danger'], fg=COLOR_PALETTE['white'],
              font=FONTS['label'], width=12, bd=0
              ).pack(side='left', padx=10)

    dialog.protocol("WM_DELETE_WINDOW", on_cancel)
    username_entry.focus()
    dialog.mainloop()
    # Destruir root para evitar ventana fantasma
    try:
        root.destroy()
    except Exception:
        pass
    return result['success'] 
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox

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
    dialog.title("Inicio de Sesión")
    _center_window(dialog, 350, 220)
    dialog.resizable(False, False)

    Label(dialog, text=f"🔐 Autenticación - {role_info.get('nombre', '')}", font=('Arial', 14, 'bold')).pack(pady=(10, 20))

    Label(dialog, text="Usuario:").pack(anchor='w', padx=20)
    username_entry = Entry(dialog)
    username_entry.pack(fill='x', padx=20, pady=5)

    Label(dialog, text="Contraseña:").pack(anchor='w', padx=20)
    password_entry = Entry(dialog, show='*')
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

    btn_frame = Button(dialog, text="Ingresar", command=on_accept)
    btn_frame.pack(pady=10)

    Button(dialog, text="Cancelar", command=on_cancel).pack()

    dialog.protocol("WM_DELETE_WINDOW", on_cancel)
    username_entry.focus()
    dialog.mainloop()
    # Destruir root para evitar ventana fantasma
    try:
        root.destroy()
    except Exception:
        pass
    return result['success'] 
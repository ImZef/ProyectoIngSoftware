"""
Constants and theme configuration for AgroVet Plus GUI.
"""

# Paleta de colores temática
COLOR_PALETTE = {
    'primary': '#2E8B57',      # Verde bosque
    'secondary': '#90EE90',     # Verde claro
    'accent': '#FFD700',        # Dorado
    'danger': '#FF6B6B',        # Rojo coral
    'success': '#4CAF50',       # Verde éxito
    'white': '#FFFFFF',
    'light_gray': '#F5F5F5',
    'dark_gray': '#2F2F2F'
}

# Configuración de fuentes
FONTS = {
    'title': ('Arial', 28, 'bold'),
    'subtitle': ('Arial', 14, 'italic'),
    'header': ('Arial', 16, 'bold'),
    'label': ('Arial', 11, 'bold'),
    'text': ('Arial', 10),
    'small': ('Arial', 9)
}

# Iconos emoji para la aplicación
ICONS = {
    'vet': '🐄🐕',
    'dashboard': '📊',
    'inventory': '📦',
    'products': '🏷️',
    'history': '📋',
    'clinical': '🩺',
    'sales': '💰',
    'appointments': '📅',  # Nuevo icono para el módulo de citas
    'users': '👥',         # Nuevo icono para el módulo de gestión de usuarios
    'request': '📄',       # Icono para registrar solicitudes
    'receipt': '🧾',       # Icono para comprobantes de venta
    'add': '➕',
    'edit': '✏️',
    'update': '🔄',
    'search': '🔍',
    'save': '✅',
    'cancel': '❌',
    'close': '❌',
    'warning': '⚠️',
    'success': '✅',
    'error': '❌',
    'info': 'ℹ️'
}

# Configuración de ventana
WINDOW_CONFIG = {
    'main_size': '1200x800',
    'dialog_size': '500x400',
    'small_dialog_size': '400x300'
}

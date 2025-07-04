# GUI package
"""
Paquete GUI para AgroVet Plus

Este archivo __init__.py convierte el directorio GUI en un paquete Python,
permitiendo importar módulos desde él usando imports relativos.

Funciones principales del __init__.py:
1. Indica a Python que este directorio es un paquete
2. Permite imports como: from GUI import main_app
3. Puede definir qué se exporta cuando se hace: from GUI import *
4. Puede ejecutar código de inicialización del paquete
5. Facilita la organización modular del código

En este proyecto, permite que:
- launcher.py pueda importar: from GUI.gui_agroveterinaria import main
- Los módulos internos usen imports relativos: from .config import COLOR_PALETTE
- Se mantenga la estructura organizativa de componentes separados
"""

# Importaciones principales del paquete
from .app import AgrovetApplication, main
from .configuracion import COLOR_PALETTE, FONTS, ICONS

# Define qué se exporta cuando se hace "from GUI import *"
__all__ = [
    'main',
    'AgrovetApplication',
    'COLOR_PALETTE',
    'FONTS', 
    'ICONS'
]

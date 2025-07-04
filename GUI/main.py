"""
AgroVet Plus GUI Application

Este archivo ha sido refactorizado en componentes separados para mejorar
la organización del código y facilitar el mantenimiento.

Archivos principales:
- main_app.py: Aplicación principal
- config.py: Configuración y constantes  
- dashboard.py: Componente del dashboard
- inventory.py: Componente del inventario
- clinical.py: Componente de historiales clínicos
- dialogs.py: Ventanas de diálogo
"""

# Importar la aplicación principal desde el nuevo módulo
from .app import main

# Exportar main para compatibilidad
__all__ = ['main']

# Mantener compatibilidad con imports anteriores
if __name__ == "__main__":
    main()
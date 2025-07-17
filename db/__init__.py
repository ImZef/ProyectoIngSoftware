"""
Database module for AgroVet Plus - Centralizes all JSON data file management.
"""

import os
from typing import Dict, Any

# Rutas de archivos de base de datos
DB_DIR = "db"
DB_FILES = {
    'productos': os.path.join(DB_DIR, "productos.json"),
    'historiales': os.path.join(DB_DIR, "historiales.json"),
    'historial_stock': os.path.join(DB_DIR, "historial_stock.json"),
    'ventas': os.path.join(DB_DIR, "ventas.json"),
    'solicitudes': os.path.join(DB_DIR, "solicitudes.json"),
}

def get_db_path(file_key: str) -> str:
    """
    Obtener la ruta de un archivo de base de datos.
    
    Args:
        file_key: Clave del archivo ('productos', 'historiales', etc.)
        
    Returns:
        str: Ruta completa al archivo
        
    Raises:
        KeyError: Si la clave no existe
    """
    if file_key not in DB_FILES:
        raise KeyError(f"Archivo de BD '{file_key}' no encontrado. Disponibles: {list(DB_FILES.keys())}")
    
    return DB_FILES[file_key]

def ensure_db_directory() -> None:
    """Asegurar que el directorio de base de datos existe."""
    os.makedirs(DB_DIR, exist_ok=True)

def get_all_db_files() -> Dict[str, str]:
    """Obtener todas las rutas de archivos de base de datos."""
    return DB_FILES.copy()

def initialize_db() -> None:
    """Inicializar la base de datos creando el directorio si no existe."""
    ensure_db_directory()
    print(f"📁 Directorio de base de datos inicializado: {DB_DIR}")

# Inicializar automáticamente al importar
initialize_db()

__all__ = ["get_db_path", "ensure_db_directory", "get_all_db_files", "initialize_db", "DB_FILES"] 
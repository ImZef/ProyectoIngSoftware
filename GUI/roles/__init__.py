"""Paquete que agrupa la lógica y vistas específicas de cada rol.

Estructura sugerida:
    GUI/roles/
        auxiliar/
        bodeguero/
        veterinario/
        administrador/

Cada subpaquete contendrá componentes, ventanas o utilidades exclusivas
para el rol correspondiente, de modo que el código del núcleo de la GUI
permanezca limpio y escalable.
"""

import importlib
import pkgutil
from typing import Dict


def _collect_role_info() -> Dict[str, dict]:
    """Explorar subpaquetes y recolectar la información de roles.

    Retorna un diccionario con la forma {id: ROLE_INFO}.
    """
    roles: Dict[str, dict] = {}
    pkg_name = __name__
    for _, mod_name, is_pkg in pkgutil.iter_modules(__path__):
        if not is_pkg:
            continue
        full_name = f"{pkg_name}.{mod_name}"
        try:
            module = importlib.import_module(full_name)
            info = getattr(module, "ROLE_INFO", None)
            if info and isinstance(info, dict):
                roles[str(info.get("id"))] = info
        except Exception:
            # Si un módulo falla al importar lo ignoramos para no interrumpir la aplicación
            continue
    return roles


AVAILABLE_ROLES: Dict[str, dict] = _collect_role_info()

# Importar funciones y clases principales de roles
from .role_selection import create_role_selection_window
from .manager import role_manager, RoleManager

__all__ = ["AVAILABLE_ROLES", "create_role_selection_window", "role_manager", "RoleManager"] 
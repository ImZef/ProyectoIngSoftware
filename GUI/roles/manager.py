"""
Role manager for centralized role handling in AgroVet Plus.
"""

from typing import Dict, Optional, Tuple, Any
from . import AVAILABLE_ROLES
from .role_selection import create_role_selection_window


class RoleManager:
    """Gestor centralizado para el manejo de roles en la aplicación."""
    
    def __init__(self):
        self.available_roles = AVAILABLE_ROLES
        self.current_role: Optional[Dict[str, Any]] = None
        self.current_interface: str = 'gui'
    
    def get_available_roles(self) -> Dict[str, dict]:
        """Obtener todos los roles disponibles."""
        return self.available_roles
    
    def get_role_by_id(self, role_id: str) -> Optional[Dict[str, Any]]:
        """Obtener un rol específico por su ID."""
        return self.available_roles.get(role_id)
    
    def get_role_permissions(self, role_id: str) -> list:
        """Obtener los permisos de un rol específico."""
        role = self.get_role_by_id(role_id)
        return role.get('permisos', []) if role else []
    
    def has_permission(self, permission: str, role_id: str = None) -> bool:
        """Verificar si un rol tiene un permiso específico."""
        if role_id is None and self.current_role:
            role_id = str(self.current_role.get('id'))
        
        if not role_id:
            return False
            
        permissions = self.get_role_permissions(role_id)
        return permission in permissions or 'todas_las_funciones' in permissions
    
    def select_role_interactively(self) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Mostrar ventana de selección de rol y retornar el rol e interfaz seleccionados."""
        result = create_role_selection_window()
        
        if result and result != (None, None):
            role, interface = result
            self.current_role = role
            self.current_interface = interface
            return role, interface
        
        return None, None
    
    def set_current_role(self, role: Dict[str, Any], interface: str = 'gui') -> None:
        """Establecer el rol actual."""
        self.current_role = role
        self.current_interface = interface
    
    def get_current_role(self) -> Optional[Dict[str, Any]]:
        """Obtener el rol actual."""
        return self.current_role
    
    def get_current_interface(self) -> str:
        """Obtener la interfaz actual."""
        return self.current_interface
    
    def validate_role_access(self, required_permissions: list) -> bool:
        """Validar si el rol actual tiene acceso a las funcionalidades requeridas."""
        if not self.current_role:
            return False
            
        current_permissions = self.current_role.get('permisos', [])
        
        # Si tiene todas las funciones, acceso completo
        if 'todas_las_funciones' in current_permissions:
            return True
            
        # Verificar si tiene al menos uno de los permisos requeridos
        return any(perm in current_permissions for perm in required_permissions)
    
    def get_accessible_tabs(self) -> Dict[str, bool]:
        """Retornar qué pestañas son accesibles para el rol actual."""
        if not self.current_role:
            return {
                'dashboard': True,
                'inventory': False,
                'clinical_history': False,
                'sales': False,
                'appointments': False,
                'products': False,
                'history': False,
                'user_management': False
            }
        
        permissions = self.current_role.get('permisos', [])
        
        return {
            'dashboard': True,  # Siempre visible
            'inventory': any(p in permissions for p in ['inventario', 'stock', 'productos', 'todas_las_funciones']),
            'clinical_history': any(p in permissions for p in ['historiales_clinicos', 'todas_las_funciones']),
            'sales': any(p in permissions for p in ['ventas', 'todas_las_funciones']),
            'appointments': any(p in permissions for p in ['ventas', 'todas_las_funciones']),
            'products': 'todas_las_funciones' in permissions,
            'history': 'todas_las_funciones' in permissions,
            'user_management': 'todas_las_funciones' in permissions,
            'orders': any(p in permissions for p in ['pedidos', 'todas_las_funciones'])
        }
    
    def get_role_description(self, role_id: str = None) -> str:
        """Obtener descripción del rol."""
        if role_id is None and self.current_role:
            role_id = str(self.current_role.get('id'))
            
        role = self.get_role_by_id(role_id)
        if role:
            return f"{role.get('nombre', 'Rol desconocido')} - {', '.join(role.get('permisos', []))}"
        return "Rol no encontrado"
    
    def reset_role(self) -> None:
        """Reiniciar el rol actual."""
        self.current_role = None
        self.current_interface = 'gui'


# Instancia global del gestor de roles
role_manager = RoleManager() 
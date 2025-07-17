"""Módulos y componentes específicos para el rol de Bodeguero."""
ROLE_INFO = {
    "id": "2",
    "nombre": "Bodeguero",
    # Permisos ampliados: ahora incluye gestión de pedidos
    "permisos": ["inventario", "stock", "productos", "consulta_ventas", "pedidos"],
}
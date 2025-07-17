"""
Paquete específico para el rol de Médico Veterinario.
Contiene funcionalidades exclusivas del veterinario.
"""

# Información del rol
ROLE_INFO = {
    "id": "veterinario",
    "nombre": "Médico Veterinario",
    "descripcion": "Profesional veterinario con acceso completo a historiales clínicos",
    "permisos": [
        "historiales_clinicos",
        "consultar_historial_completo",
        "crear_historiales", 
        "editar_historiales",
        "generar_recomendaciones"
    ],
    "funcionalidades_especificas": [
        "Consultar historial clínico completo del cliente",
        "Ver detalles de consultas anteriores",
        "Acceder a historial de compras para recomendaciones",
        "Generar recomendaciones personalizadas"
    ]
}

__all__ = ["ROLE_INFO"] 
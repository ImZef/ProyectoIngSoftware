"""
HU13: Ver alertas de stock bajo
Gestión de alertas de inventario
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

from .Inventario import Inventario, Producto

UMBRAL_DEFECTO = 5
RUTA_UMBRAL_JSON = Path("db/stock_thresholds.json")
RUTA_ALERTAS_JSON = Path("db/stock_alerts.json")


def _cargar_json(ruta: Path, defecto):
    try:
        if ruta.exists():
            with open(ruta, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return defecto


def _guardar_json(ruta: Path, data):
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception:
        pass


class AlertasStockManager:
    """Lógica de negocio para alertas de stock bajo (HU13)."""

    def __init__(self, inventario: Inventario):
        self.inventario = inventario
        # Cargar umbrales por producto {codigo: umbral}
        self.umbrales: Dict[str, int] = _cargar_json(RUTA_UMBRAL_JSON, {})
        # Cargar últimos productos alertados para generar notificaciones
        self.ultimo_alertado: List[str] = _cargar_json(RUTA_ALERTAS_JSON, [])

    # ---------------- Funcionalidades principales -----------------
    def obtener_umbral(self, codigo_producto: int) -> int:
        """Obtener umbral configurado para un producto (o global por defecto)."""
        return self.umbrales.get(str(codigo_producto), UMBRAL_DEFECTO)

    def configurar_umbral_producto(self, codigo_producto: int, nuevo_umbral: int):
        """Configurar el nivel mínimo de stock para un producto específico."""
        if nuevo_umbral < 0:
            raise ValueError("El umbral no puede ser negativo")
        self.umbrales[str(codigo_producto)] = int(nuevo_umbral)
        _guardar_json(RUTA_UMBRAL_JSON, self.umbrales)

    def listar_productos_bajo_stock(self) -> List[Producto]:
        """Listar todos los productos cuyo stock está por debajo de su umbral."""
        productos_bajos = []
        for producto in self.inventario.productos:
            if producto.get_cantidad() < self.obtener_umbral(producto.get_codigo()):
                productos_bajos.append(producto)
        return productos_bajos

    def detectar_nuevas_alertas(self) -> Tuple[List[Producto], List[Producto]]:
        """Detectar nuevos productos que acaban de caer por debajo del umbral.
        Retorna (nuevos_alertas, vigentes).
        """
        vigentes = self.listar_productos_bajo_stock()
        codigos_vigentes = {str(p.get_codigo()) for p in vigentes}
        nuevos = [p for p in vigentes if str(p.get_codigo()) not in self.ultimo_alertado]
        # Actualizar registro
        self.ultimo_alertado = list(codigos_vigentes)
        _guardar_json(RUTA_ALERTAS_JSON, self.ultimo_alertado)
        return nuevos, vigentes

    # ---------------- Utilidades -----------------
    def exportar_alertas_actuales(self) -> List[Dict]:
        """Exportar alertas actuales en formato dict para UI o reportes."""
        alertas = []
        for p in self.listar_productos_bajo_stock():
            alertas.append({
                "codigo": p.get_codigo(),
                "nombre": p.get_nombre(),
                "stock": p.get_cantidad(),
                "umbral": self.obtener_umbral(p.get_codigo())
            })
        return alertas 
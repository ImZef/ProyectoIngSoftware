"""Compatibilidad temporal.
Reexporta las constantes de GUI.configuracion para que módulos que
importan `from .configuracion` sigan funcionando aun cuando el código
haya sido movido.
Una vez todos los import relativos se actualicen, este archivo se puede
eliminar.
"""

from ..configuracion import * 
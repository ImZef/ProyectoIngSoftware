"""
Módulo para gestionar usuarios y sus roles.
"""
import json
from pathlib import Path
from typing import List, Dict

class Usuario:
    def __init__(self, username: str, nombre: str, rol_id: str):
        self.username = username
        self.nombre = nombre
        self.rol_id = rol_id

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "nombre": self.nombre,
            "rol_id": self.rol_id,
        }

class GestorUsuarios:
    def __init__(self, archivo_usuarios: str = "db/usuarios.json"):
        from pathlib import Path
        self.archivo = Path(archivo_usuarios)
        self.archivo.parent.mkdir(parents=True, exist_ok=True)
        self.usuarios: List[Usuario] = []
        self._cargar_usuarios()

    def _cargar_usuarios(self):
        if not self.archivo.exists():
            return
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
            for u in data:
                self.usuarios.append(Usuario(u.get("username"), u.get("nombre"), u.get("rol_id")))
        except Exception:
            self.usuarios.clear()

    def _guardar_usuarios(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in self.usuarios], f, indent=4, ensure_ascii=False)

    def listar_usuarios(self) -> List[Usuario]:
        return self.usuarios

    def agregar_usuario(self, username: str, nombre: str, rol_id: str) -> Usuario:
        if any(u.username == username for u in self.usuarios):
            raise ValueError("El usuario ya existe")
        usuario = Usuario(username, nombre, rol_id)
        self.usuarios.append(usuario)
        self._guardar_usuarios()
        return usuario

    def actualizar_rol(self, username: str, nuevo_rol_id: str) -> Usuario:
        usuario = next((u for u in self.usuarios if u.username == username), None)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        usuario.rol_id = nuevo_rol_id
        self._guardar_usuarios()
        return usuario

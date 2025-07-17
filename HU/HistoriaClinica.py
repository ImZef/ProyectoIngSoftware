# HU/HistoriaClinica.py
import json
from datetime import datetime
from pathlib import Path

class HistoriaClinica:
    historiales = []  # Lista de objetos de historia clínica

    def __init__(self, id_cliente, nombre_cliente, nombre_mascota):
        self._id_cliente = id_cliente
        self._nombre_cliente = nombre_cliente
        self._nombre_mascota = nombre_mascota
        self._registros = []
        # La siguiente línea se elimina para que el constructor no modifique la lista global.
        # HistoriaClinica.historiales.append(self)

    def get_id_cliente(self): return self._id_cliente
    def get_nombre_cliente(self): return self._nombre_cliente
    def get_nombre_mascota(self): return self._nombre_mascota
    def get_registros(self): return self._registros

    def registrar_diagnostico(self, diagnostico, tratamiento, comentarios=""):
        if not diagnostico or not tratamiento:
            raise ValueError("Diagnóstico y tratamiento son campos obligatorios")

        registro = {
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "hora": datetime.now().strftime("%H:%M:%S"),
            "diagnostico": diagnostico,
            "tratamiento": tratamiento,
            "comentarios": comentarios
        }
        self._registros.append(registro)

    # ---------- Serialización ----------
    def to_dict(self):
        """Convertir el historial a un diccionario serializable."""
        return {
            "id_cliente": self._id_cliente,
            "nombre_cliente": self._nombre_cliente,
            "nombre_mascota": self._nombre_mascota,
            "registros": self._registros
        }

    def ver_historial(self):
        print(f"\nHistorial clínico de {self._nombre_mascota} (Cliente: {self._nombre_cliente}) (ID: {self._id_cliente}):")
        if not self._registros:
            print("No hay registros aún.")
        for i, reg in enumerate(self._registros, 1):
            print(f"\nRegistro {i}")
            for k, v in reg.items():
                print(f"{k.capitalize()}: {v}")

    @classmethod
    def buscar_historial(cls, id_cliente):
        return next((h for h in cls.historiales if h.get_id_cliente() == id_cliente), None)

    @classmethod
    def crear_o_actualizar_historial(cls):
        def entrada(msg, val=lambda x: True, err="Entrada inválida", opcional=False):
            while True:
                dato = input(msg).strip()
                if opcional and not dato:
                    return ""
                if val(dato):
                    return dato
                print(err)

        id_cliente = entrada("ID del cliente: ", str.isdigit, "Debe ser numérico")
        historial = cls.buscar_historial(id_cliente)

        if historial:
            print("Historial encontrado. Agregando registro...")
        else:
            print("No se encontró historial para este cliente.")
            crear_nuevo = input("¿Desea crear un nuevo cliente? (s/n): ").strip().lower()
            if crear_nuevo != 's':
                print("Operación cancelada.")
                return

            nombre_cliente = entrada("Nombre del cliente: ", lambda s: s != "", "Requerido")
            nombre_mascota = entrada("Nombre de la mascota: ", lambda s: s != "", "Requerido")
            historial = cls(id_cliente, nombre_cliente, nombre_mascota)
            cls.historiales.append(historial)  # Añadir explícitamente a la lista
            print("Historial creado para el cliente.")

        diagnostico = entrada("Diagnóstico: ", lambda s: s != "", "Requerido")
        tratamiento = entrada("Tratamiento: ", lambda s: s != "", "Requerido")
        comentarios = entrada("Comentarios (opcional): ", opcional=True)

        try:
            historial.registrar_diagnostico(diagnostico, tratamiento, comentarios)
            print("\n Diagnóstico y tratamiento registrados exitosamente.")
        except ValueError as e:
            print(f"Error: {e}")

        historial.ver_historial()
        cls.guardar_historiales()

    @classmethod
    def ver_historiales(cls):
        if not cls.historiales:
            print("No hay historiales clínicos registrados.")
            return
        for h in cls.historiales:
            h.ver_historial()

    @classmethod
    def guardar_historiales(cls, archivo="db/historiales.json"):
        """Guardar todos los historiales en un archivo JSON."""
        try:
            # Asegurarse de que el directorio de la base de datos exista
            Path(archivo).parent.mkdir(parents=True, exist_ok=True)
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump([h.to_dict() for h in cls.historiales], f, indent=4, ensure_ascii=False)
            print(f"Historiales guardados en {archivo}")
        except Exception as e:
            print(f"Error al guardar historiales: {e}")

    @classmethod
    def cargar_historiales(cls, archivo="db/historiales.json"):
        if cls.historiales:  # Si ya hay datos, no cargar de nuevo en la misma sesión.
            return

        try:
            if not Path(archivo).exists():
                print(f"Archivo {archivo} no encontrado. Creando historiales de muestra.")
                cls._crear_historiales_muestra()
                cls.guardar_historiales(archivo)
                return

            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
                if not contenido or contenido == '[]':
                    # No es necesario crear datos de muestra si el usuario empieza a registrar.
                    # Se creará el archivo al guardar el primer historial.
                    print(f"Archivo {archivo} vacío o sin historiales.")
                    return
            
            datos = json.loads(contenido)
            
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar desde {archivo}: {e}. Se iniciará la sesión sin historiales.")
            cls.historiales.clear()
            return

        # Si llegamos aquí, 'datos' tiene contenido válido.
        temp_historiales = []
        for h in datos:
            nuevo = cls(h["id_cliente"], h["nombre_cliente"], h["nombre_mascota"])
            nuevo._registros = h.get("registros", [])
            temp_historiales.append(nuevo)
        
        # Solo ahora modificamos la lista de la clase
        cls.historiales.clear()
        cls.historiales.extend(temp_historiales)
        print(f"Historiales cargados desde {archivo}")

    @classmethod
    def _crear_historiales_muestra(cls):
        """Crear historiales de ejemplo para primeros usos."""
        if cls.historiales:
            return
        muestras = [
            ("1", "Pedro Gómez", "Milagros",
             "Deficiencia de vitaminas", "Vitamina AD3E Inyectable", "Aplicar 10 ml intramuscular una vez por semana durante 3 semanas"),
            ("2", "Laura Sánchez", "Tornado",
             "Infestación por parásitos internos", "Ivermectina 1%", "Administrar 1 ml por cada 50 kg de peso vivo vía subcutánea"),
            ("3", "Carlos Rivas", "Rocky",
             "Infección bacteriana de piel", "Antibiótico Tilmicosina", "Administrar 1 ml por cada 30 kg, cada 72 horas durante una semana")
        ]
        for idc, nom, mas, diag, trat, com in muestras:
            h = HistoriaClinica(idc, nom, mas)
            h.registrar_diagnostico(diag, trat, com)
            cls.historiales.append(h)

    @classmethod
    def get_next_id(cls):
        if not cls.historiales:
            return 1
        return max(int(h.get_id_cliente()) for h in cls.historiales if str(h.get_id_cliente()).isdigit()) + 1

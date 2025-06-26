# HU/HistoriaClinica.py
import json
from datetime import datetime

class HistoriaClinica:
    historiales = []  # Lista de objetos de historia clínica

    def __init__(self, id_cliente, nombre_cliente, nombre_mascota):
        self._id_cliente = id_cliente
        self._nombre_cliente = nombre_cliente
        self._nombre_mascota = nombre_mascota
        self._registros = []
        HistoriaClinica.historiales.append(self)

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
    def guardar_historiales(cls, archivo="historiales.json"):
        datos = []
        for h in cls.historiales:
            datos.append({
                "id_cliente": h.get_id_cliente(),
                "nombre_cliente": h.get_nombre_cliente(),
                "nombre_mascota": h.get_nombre_mascota(),
                "registros": h.get_registros()
            })
        with open(archivo, "w") as f:
            json.dump(datos, f, indent=4)

    @classmethod
    def cargar_historiales(cls, archivo="historiales.json"):
        try:
            with open(archivo, "r") as f:
                datos = json.load(f)
                for h in datos:
                    nuevo = HistoriaClinica(h["id_cliente"], h["nombre_cliente"], h["nombre_mascota"])
                    for r in h["registros"]:
                        nuevo._registros.append(r)
            print(f" Historiales cargados desde {archivo}")
        except FileNotFoundError:
            print(f" Archivo {archivo} no encontrado. Se iniciará sin historiales.")

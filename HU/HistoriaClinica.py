from datetime import datetime

class HistoriaClinica:
    historiales = []  # Lista de objetos de historia clínica

    def __init__(self, id_cliente, nombre_cliente, nombre_mascota):
        self._id_cliente = id_cliente
        self._nombre_cliente = nombre_cliente
        self._nombre_mascota = nombre_mascota
        self._registros = []
        HistoriaClinica.historiales.append(self)

    # Getters y setters
    def get_id_cliente(self):
        return self._id_cliente
    
    def set_id_cliente(self, id_cliente):
        self._id_cliente = id_cliente
    
    def get_nombre_cliente(self):
        return self._nombre_cliente
    
    def set_nombre_cliente(self, nombre_cliente):
        self._nombre_cliente = nombre_cliente
        
    def get_nombre_mascota(self):
        return self._nombre_mascota
    
    def set_nombre_mascota(self, nombre_mascota):
        self._nombre_mascota = nombre_mascota
        
    def get_registros(self):
        return self._registros
    
    def registrar_diagnostico(self, diagnostico, tratamiento, comentarios=""):
        if not diagnostico or not tratamiento:
            raise ValueError("Diagnóstico y tratamiento son campos obligatorios")

        registro = {
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "diagnostico": diagnostico,
            "tratamiento": tratamiento,
            "comentarios": comentarios
        }

        self._registros.append(registro)
        print("Registro clínico agregado con éxito.\n")
        
    def ver_historial(self):
        print(f"\nHistorial clínico de {self._nombre_mascota} (Cliente: {self._nombre_cliente}) (ID: {self._id_cliente}):")
        if not self._registros:
            print("No hay registros aún.")
            return
        for i, reg in enumerate(self._registros, 1):
            print(f"\nRegistro {i}")
            print(f"Fecha: {reg['fecha']}")
            print(f"Hora: {reg['Hora']}")   
            print(f"Diagnóstico:  {reg['diagnostico']}")
            print(f"Tratamiento:  {reg['tratamiento']}")
            print(f"Comentarios:  {reg['comentarios']}")
    
    @classmethod
    def ver_historiales(cls):
        if not cls.historiales:
            print("No hay historiales clínicos registrados.")
            return
        
        count = 1
        for historial in cls.historiales:   
            print(f"\nHistorial clínico de {historial.get_nombre_mascota()} (Cliente: {historial.get_nombre_cliente()}) (ID: {historial.get_id_cliente()}):")
            
            registros = historial.get_registros()
            if not registros:
                print("No hay registros aún.")
            else:
                for reg in registros:
                    print(f"\nRegistro {count}")
                    print(f"Fecha: {reg['fecha']}")
                    print(f"Hora: {reg['Hora']}")
                    print(f"Diagnóstico:  {reg['diagnostico']}")
                    print(f"Tratamiento:  {reg['tratamiento']}")
                    print(f"Comentarios:  {reg['comentarios']}")
                    count += 1
    
    @classmethod
    def buscar_historial(cls, id_cliente):
        for historial in cls.historiales:
            if historial.get_id_cliente() == id_cliente:
                return historial
        return None
    
    @classmethod  
    def crear_o_actualizar_historial(cls):
        def _prompt_until_valid(prompt, validator, error_msg, allow_empty=False):
            while True:
                valor = input(prompt).strip()
                if not valor and allow_empty:
                    return ""
                if validator(valor):
                    return valor
                print(error_msg)

        id_cliente = _prompt_until_valid(
            "Ingrese el ID del cliente: ",
            lambda s: s.isdigit(),
            "El ID debe ser un número."
        )
        nombre_mascota = _prompt_until_valid(
            "Ingrese el nombre de la mascota: ",
            lambda s: bool(s),
            "El nombre de la mascota no puede estar vacío."
        )
        diagnostico = _prompt_until_valid(
            "Ingrese el diagnóstico: ",
            lambda s: bool(s),
            "El diagnóstico no puede estar vacío."
        )
        tratamiento = _prompt_until_valid(
            "Ingrese el tratamiento: ",
            lambda s: bool(s),
            "El tratamiento no puede estar vacío."
        )
        comentarios = input("Comentarios adicionales (opcional): ").strip()

        historial = cls.buscar_historial(id_cliente)

        if historial:
            print("Se encontró historial existente. Agregando nuevo registro...")
        else:
            nombre_cliente = _prompt_until_valid(
                "Ingrese el nombre del cliente: ",
                lambda s: bool(s),
                "El nombre del cliente no puede estar vacío."
            )
            historial = HistoriaClinica(id_cliente, nombre_cliente, nombre_mascota)
            print("Historial clínico creado para el cliente.")

        try:
            historial.registrar_diagnostico(diagnostico, tratamiento, comentarios)
        except ValueError as e:
            print(f"Error: {e}")

        historial.ver_historial()

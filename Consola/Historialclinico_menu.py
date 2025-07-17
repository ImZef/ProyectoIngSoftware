from HU.HistoriaClinica import HistoriaClinica

class MenuHistorialClinico:
    @staticmethod
    def mostrar_menu():
        # Cargar historiales existentes desde JSON
        HistoriaClinica.cargar_historiales()
        while True:
            print("\n--- Menú de Historial Clínico ---")
            print("1. Registrar diagnóstico y tratamiento")
            print("2. Consultar historial de un cliente")
            print("3. Mostrar todos los historiales")
            print("0. Volver al menú principal")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                HistoriaClinica.crear_o_actualizar_historial()
                # Guardar al disco tras cambios
                HistoriaClinica.guardar_historiales()

            elif opcion == "2":
                id_cliente = input("Ingrese el ID del cliente a consultar: ")
                historial = HistoriaClinica.buscar_historial(id_cliente)
                if historial:
                    historial.ver_historial()
                else:
                    print("No se encontró historial con ese ID.")

            elif opcion == "3":
                HistoriaClinica.ver_historiales()

            elif opcion == "0":
                print("Volviendo al menú principal...")
                # Guardar antes de salir
                HistoriaClinica.guardar_historiales()
                break

            else:
                print("Opción inválida. Por favor intente nuevamente.")

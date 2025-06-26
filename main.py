from Producto import Producto, main as producto_main
from Registrar import HistoriaClinica, main as historial_main
from Venta import menu_ventas

# Datos de muestra para productos
producto1 = Producto(1, "Leche", "Lácteos", "Leche entera 1L", 4000, 20, "19/08/2025")
producto2 = Producto(2, "Pan", "Panadería", "Pan integral", 12000, 0, "22/06/2025")
producto3 = Producto(3, "Atún", "Conservas", "Lata de atún en agua", 10000, 15, "01/01/2026")
producto4 = Producto(4, "Pan artesano", "Panadería", "Pan artesanal", 15000, 3, "02/07/2025")

# Datos de muestra para historiales clínicos
historia1 = HistoriaClinica("1", "Juan Pérez", "Firulais")
historia1.registrar_diagnostico("Gripe canina", "Antibióticos", "Observación durante 48 horas")

historia2 = HistoriaClinica("2", "María López", "Michi")
historia2.registrar_diagnostico("Infección urinaria", "Antibióticos", "Dieta especial")

def main():
    print("\n¡Bienvenido al Sistema Veterinario!")
    
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Sistema de Inventario (Productos)")
        print("2. Sistema de Historial Clínico")
        print("3. Menú de Ventas")
        print("0. Salir")
        
        opcion = input("Seleccione una opción (1-3): ")
        
        if opcion == "1":
            print("\nAccediendo al sistema de inventario...")
            producto_main()
        elif opcion == "2":
            print("\nAccediendo al sistema de historial clínico...")
            historial_main()
        elif opcion == "3":
            print("\nAccediendo al menú de ventas...")
            menu_ventas()
        elif opcion == "0":
            print("\n¡Gracias por usar el Sistema Veterinario! Hasta pronto.")
            break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()

from Producto import Producto
from Inventario import Inventario
from Inventario_menu import MenuInventario
from Registrar import HistoriaClinica, main as historial_main
from Venta import Venta
from Venta_menu import MenuVentas

# Crear el inventario
mi_inventario = Inventario()

# ====== Datos de muestra para productos ======
producto1 = Producto(121, "Ivermectina 1%", "Desparasitante", "Antiparasitario inyectable de amplio espectro", 150000, 20, "19/08/2027")
producto2 = Producto(122, "Vitamina AD3E Inyectable", "Suplemento", "Suplemento vitamínico para bovinos y equinos", 120000, 30, "10/03/2026")
producto3 = Producto(123, "Antibiótico Tilmicosina", "Medicamento", "Antibiótico de amplio espectro para ganado", 180000, 15, "05/12/2025")
producto4 = Producto(124, "Concentrado Purina Bovino 40kg", "Alimento", "Alimento balanceado para engorde de ganado", 180000, 50, "15/02/2026")
producto5 = Producto(125, "Vacuna Triple Viral", "Vacuna", "Vacuna canina contra moquillo, hepatitis y parvovirus", 60000, 25, "01/09/2026")
producto6 = Producto(126, "Shampoo Antipulgas", "Higiene", "Champú especializado para control de pulgas en mascotas", 35000, 40, "20/05/2027")
producto7 = Producto(127, "Desparasitante Fenbendazol 10%", "Desparasitante", "Antiparasitario interno para bovinos", 90000, 18, "07/07/2026")
producto8 = Producto(128, "Insecticida Pour-on", "Control de plagas", "Solución tópica para control de moscas y garrapatas", 130000, 22, "11/11/2025")
producto9 = Producto(129, "Termómetro Digital Veterinario", "Herramienta", "Instrumento de medición de temperatura animal", 45000, 10, "N/A")
producto10 = Producto(130, "Sales Mineralizadas 25kg", "Suplemento", "Mezcla mineral para mejorar la nutrición en pastoreo", 70000, 35, "30/08/2026")

# Agregar productos al inventario
mi_inventario.agregar_producto(producto1)
mi_inventario.agregar_producto(producto2)
mi_inventario.agregar_producto(producto3)
mi_inventario.agregar_producto(producto4)
mi_inventario.agregar_producto(producto5)
mi_inventario.agregar_producto(producto6)
mi_inventario.agregar_producto(producto7)
mi_inventario.agregar_producto(producto8)
mi_inventario.agregar_producto(producto9)
mi_inventario.agregar_producto(producto10)

# ====== Datos de muestra para historiales clínicos ======
historia3 = HistoriaClinica("3", "Pedro Gómez", "Milagros")
historia3.registrar_diagnostico(
    "Deficiencia de vitaminas",
    "Vitamina AD3E Inyectable",
    "Aplicar 10 ml intramuscular una vez por semana durante 3 semanas"
)

historia4 = HistoriaClinica("4", "Laura Sánchez", "Tornado")
historia4.registrar_diagnostico(
    "Infestación por parásitos internos",
    "Ivermectina 1%",
    "Administrar 1 ml por cada 50 kg de peso vivo vía subcutánea"
)

historia5 = HistoriaClinica("5", "Carlos Rivas", "Rocky")
historia5.registrar_diagnostico(
    "Infección bacteriana de piel",
    "Antibiótico Tilmicosina",
    "Administrar 1 ml por cada 30 kg, una vez cada 72 horas durante una semana"
)

historia6 = HistoriaClinica("6", "María López", "Michi")
historia6.registrar_diagnostico(
    "Pulgas y garrapatas",
    "Shampoo Antipulgas",
    "Aplicar cada 3 días durante dos semanas"
)

historia7 = HistoriaClinica("7", "Luis Ramírez", "Lucero")
historia7.registrar_diagnostico(
    "Anemia nutricional",
    "Sales Mineralizadas 25kg",
    "Administrar 100g al día en la ración por 30 días"
)

historia8 = HistoriaClinica("8", "Ana Torres", "Firulais Jr.")
historia8.registrar_diagnostico(
    "Garrapatas",
    "Insecticida Pour-on",
    "Aplicar sobre el lomo una vez al mes durante la temporada de lluvias"
)

# ====== Menú principal ======
def main():
    print("\n ¡Bienvenido al Sistema de Gestión Veterinaria!")

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Sistema de Inventario (Productos)")
        print("2. Sistema de Historial Clínico")
        print("3. Menú de Ventas")
        print("0. Salir")

        opcion = input("Seleccione una opción (0-3): ")

        if opcion == "1":
            print("\n Accediendo al sistema de inventario...")
            menu_inventario = MenuInventario(mi_inventario)
            menu_inventario.mostrar_menu()


        elif opcion == "2":
            print("\n Accediendo al sistema de historial clínico...")
            historial_main()

        elif opcion == "3":
            print("\n Accediendo al menú de ventas...")
            menu_ventas = MenuVentas(mi_inventario)
            menu_ventas.mostrar_menu()

        elif opcion == "0":
            print("\n Gracias por usar el Sistema Veterinario. ¡Hasta pronto!")
            break

        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()

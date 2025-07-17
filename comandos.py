from HU.Producto import Producto
from HU.Inventario import Inventario
from HU.HistoriaClinica import HistoriaClinica
from Consola.Menu_principal import MenuPrincipal

# Crear el inventario
mi_inventario = Inventario()
mi_inventario.cargar_desde_json()  

# ====== Datos de muestra solo si el inventario está vacío ======
# Crear datos de muestra solo si no existen productos ni historiales
if not mi_inventario.productos:
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

    # Agregar al inventario
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

    # Guardar después de cargar muestra inicial
    mi_inventario.guardar_en_json()

# Cargar historiales existentes desde JSON
HistoriaClinica.cargar_historiales()

# ====== Datos de muestra para historiales clínicos ======
# Crear muestras sólo si no existen historiales
if not HistoriaClinica.historiales:
    HistoriaClinica._crear_historiales_muestra()
    HistoriaClinica.guardar_historiales()

# ==== Iniciar Menú Principal ====
def main(rol_usuario=None):
    """Función principal para ejecutar la interfaz de consola con rol de usuario."""
    menu_principal = MenuPrincipal(mi_inventario, rol_usuario)
    menu_principal.mostrar_menu()
    # Guardar inventario e historiales antes de salir
    mi_inventario.guardar_en_json()
    HistoriaClinica.guardar_historiales()

if __name__ == "__main__":
    main()

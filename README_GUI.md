# 🐄🐕 AgroVet Plus - Sistema de Gestión Agroveterinaria

## 📋 Descripción
AgroVet Plus es un sistema completo de gestión para agroveterinarias que permite administrar inventarios, productos, ventas e historiales clínicos de manera eficiente y profesional.

## ✨ Características Principales

### 🖥️ Interfaz Gráfica (Nueva)
- **Dashboard Interactivo**: Vista general con estadísticas clave
- **Gestión de Inventario**: Búsqueda avanzada y visualización en tabla
- **Alertas Automáticas**: Notificaciones de stock bajo y productos agotados
- **Diseño Responsivo**: Interfaz moderna y fácil de usar
- **Colores Temáticos**: Diseño inspirado en el sector agroveterinario

### 💻 Funcionalidades
- ✅ Gestión completa de productos
- ✅ Control de inventario en tiempo real
- ✅ Historial de movimientos de stock
- ✅ Alertas de stock bajo
- ✅ Búsqueda y filtrado avanzado
- ✅ Guardado automático en JSON
- ✅ Interfaz gráfica moderna con Tkinter

## 🚀 Cómo Ejecutar

### Opción 1: Launcher (Recomendado)
```bash
python launcher.py
```
El launcher te permitirá elegir entre:
1. **Interfaz Gráfica**: Experiencia visual moderna
2. **Interfaz de Consola**: Interfaz tradicional de texto
3. **Salir**: Cerrar la aplicación

### Opción 2: Interfaz Gráfica Directa
```bash
python gui_agroveterinaria.py
```

### Opción 3: Interfaz de Consola
```bash
python main.py
```

## 📦 Dependencias
```
tkinter (incluido con Python)
pillow (para manejo de imágenes)
```

### Instalación de dependencias:
```bash
pip install pillow
```

## 🎨 Características de la Interfaz Gráfica

### 📊 Dashboard
- **Estadísticas en tiempo real**: Total de productos, agotados, stock bajo, valor total
- **Alertas visuales**: Productos que requieren atención inmediata
- **Cards informativas**: Información organizada en tarjetas coloridas

### 📦 Gestión de Inventario
- **Tabla interactiva**: Visualización completa de productos
- **Búsqueda inteligente**: Por código, nombre o categoría
- **Códigos de color**: 
  - 🟢 Verde: Producto disponible
  - 🟡 Amarillo: Stock bajo (< 5 unidades)
  - 🔴 Rojo: Producto agotado
- **Funciones disponibles**:
  - ➕ Agregar nuevos productos
  - ✏️ Actualizar stock
  - 📊 Ver historial de movimientos
  - 🔄 Actualizar vista

### 🏷️ Productos Incluidos (Muestra)
1. **Ivermectina 1%** - Desparasitante inyectable
2. **Vitamina AD3E** - Suplemento vitamínico
3. **Antibiótico Tilmicosina** - Medicamento de amplio espectro
4. **Concentrado Purina Bovino** - Alimento balanceado
5. **Vacuna Triple Viral** - Vacuna canina
6. **Shampoo Antipulgas** - Producto de higiene
7. **Desparasitante Fenbendazol** - Antiparasitario interno
8. **Insecticida Pour-on** - Control de plagas
9. **Termómetro Digital** - Herramienta veterinaria
10. **Sales Mineralizadas** - Suplemento nutricional

## 🔧 Estructura del Proyecto
```
ProyectoIngSoftware/
├── HU/                          # Lógica de negocio
│   ├── Inventario.py           # Gestión de inventario
│   ├── Producto.py             # Clase Producto
│   ├── HistoriaClinica.py      # Historiales médicos
│   └── Venta.py                # Sistema de ventas
├── Proxinterfaz/               # Interfaces de consola
├── gui_agroveterinaria.py      # 🆕 Interfaz gráfica
├── launcher.py                 # 🆕 Selector de interfaz
├── main.py                     # Punto de entrada original
├── productos.json              # Base de datos de productos
├── historial_stock.json        # Historial de movimientos
└── README.md                   # Este archivo
```

## 🎯 Ventajas de la Interfaz Gráfica

### Para el Usuario
- **Experiencia intuitiva**: Navegación fácil y visual
- **Información clara**: Datos organizados y fáciles de leer
- **Acciones rápidas**: Botones y formularios accesibles
- **Retroalimentación visual**: Colores y alertas informativas

### Para el Negocio
- **Eficiencia mejorada**: Menos tiempo en tareas administrativas
- **Reducción de errores**: Validaciones automáticas
- **Mejor control**: Vista panorámica del inventario
- **Profesionalismo**: Imagen moderna y confiable

## 🛠️ Funcionalidades Técnicas

### Persistencia de Datos
- Guardado automático en archivos JSON
- Carga automática al iniciar la aplicación
- Historial completo de movimientos

### Validaciones
- Verificación de códigos únicos
- Validación de tipos de datos
- Campos obligatorios
- Prevención de stock negativo

### Arquitectura
- **Separación de responsabilidades**: Lógica separada de interfaz
- **Reutilización**: Misma lógica para ambas interfaces
- **Escalabilidad**: Fácil agregar nuevas funcionalidades

## 📞 Soporte y Contribuciones
Para reportar problemas o sugerir mejoras, por favor contacta al equipo de desarrollo.

---
**AgroVet Plus** - Desarrollado con ❤️ para el sector agroveterinario

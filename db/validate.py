#!/usr/bin/env python3
"""
Script de validación para verificar que todas las rutas de archivos JSON
funcionan correctamente después de la reorganización.
"""

import os
import json
from . import get_db_path, get_all_db_files

def validate_db_files():
    """Validar que todos los archivos de base de datos existen y son válidos."""
    print("🔍 Validando archivos de base de datos...")
    
    all_files = get_all_db_files()
    valid_files = 0
    invalid_files = 0
    
    for file_key, file_path in all_files.items():
        print(f"\n📁 Validando {file_key}: {file_path}")
        
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            print(f"   ❌ ERROR: Archivo no encontrado")
            invalid_files += 1
            continue
        
        # Verificar que es JSON válido
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"   ✅ JSON válido - {len(data)} elementos")
            valid_files += 1
        except json.JSONDecodeError as e:
            print(f"   ❌ ERROR JSON: {e}")
            invalid_files += 1
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            invalid_files += 1
    
    print(f"\n📊 Resultado de validación:")
    print(f"   ✅ Archivos válidos: {valid_files}")
    print(f"   ❌ Archivos inválidos: {invalid_files}")
    print(f"   📁 Total de archivos: {len(all_files)}")
    
    if invalid_files == 0:
        print("   🎉 ¡Todos los archivos de BD están correctos!")
        return True
    else:
        print("   ⚠️  Hay archivos con problemas que necesitan atención.")
        return False

def check_file_structure():
    """Verificar la estructura de cada archivo JSON."""
    print("\n🏗️  Verificando estructura de archivos...")
    
    # Estructura esperada para cada tipo de archivo
    expected_structures = {
        'productos': ['codigo', 'nombre', 'categoria', 'precio', 'cantidad'],
        'historiales': ['id_cliente', 'nombre_cliente', 'nombre_mascota', 'registros'],
        'historial_stock': ['codigo_producto', 'nombre_producto', 'stock_anterior', 'nuevo_stock', 'motivo', 'fecha'],
        'ventas': ['cliente', 'forma_pago', 'fecha_venta', 'productos'],
        'solicitudes': ['cliente', 'descripcion', 'fecha']
    }
    
    for file_key, expected_keys in expected_structures.items():
        try:
            file_path = get_db_path(file_key)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data and isinstance(data, list) and len(data) > 0:
                first_item = data[0]
                missing_keys = [key for key in expected_keys if key not in first_item]
                
                if missing_keys:
                    print(f"   ⚠️  {file_key}: Faltan claves {missing_keys}")
                else:
                    print(f"   ✅ {file_key}: Estructura correcta")
            else:
                print(f"   📝 {file_key}: Archivo vacío o estructura no verificable")
                
        except Exception as e:
            print(f"   ❌ {file_key}: Error al verificar estructura - {e}")

def run_full_validation():
    """Ejecutar validación completa."""
    print("=" * 60)
    print("🔧 VALIDADOR DE BASE DE DATOS - AGROVET PLUS")
    print("=" * 60)
    
    # Validar archivos
    files_ok = validate_db_files()
    
    # Verificar estructura
    check_file_structure()
    
    print("\n" + "=" * 60)
    if files_ok:
        print("✅ VALIDACIÓN EXITOSA - Base de datos lista para usar")
    else:
        print("❌ VALIDACIÓN FALLIDA - Revisar archivos con problemas")
    print("=" * 60)
    
    return files_ok

if __name__ == "__main__":
    run_full_validation() 
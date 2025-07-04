#!/usr/bin/env python3
"""
Launcher para la aplicación AgroVet Plus
Este archivo permite ejecutar tanto la interfaz gráfica como la de consola
"""

import sys
from HU.Inventario import Inventario
from GUI.main import main as gui_main
from comandos import main as console_main

def mostrar_menu_inicial():
    print("\n" + "="*50)
    print("🐄🐕 BIENVENIDO A AGROVET PLUS 🐕🐄")
    print("="*50)
    print("Sistema de Gestión Agroveterinaria")
    print("\nSeleccione el tipo de interfaz:")
    print("1. 🖥️  Interfaz Gráfica (Recomendado)")
    print("2. 💻 Interfaz de Consola")
    print("3. ❌ Salir")
    print("="*50)

def main():
    while True:
        mostrar_menu_inicial()
        
        try:
            opcion = input("\n👉 Ingrese su opción (1-3): ").strip()
            
            if opcion == "1":
                print("\n🚀 Iniciando interfaz gráfica...")
                try:
                    
                    gui_main()
                    break
                except ImportError as e:
                    print(f"❌ Error al cargar la interfaz gráfica: {e}")
                    print("💡 Asegúrese de tener tkinter instalado")
                    input("Presione Enter para continuar...")
                except Exception as e:
                    print(f"❌ Error inesperado: {e}")
                    input("Presione Enter para continuar...")
            
            elif opcion == "2":
                print("\n💻 Iniciando interfaz de consola...")
                try:
                    # Ejecutar la función principal del main.py original
                    console_main()
                    break
                except ImportError:
                    # Si no existe main() en main.py, ejecutar directamente
                    import comandos
                    break
                except Exception as e:
                    print(f"❌ Error al cargar la interfaz de consola: {e}")
                    input("Presione Enter para continuar...")
            
            elif opcion == "3":
                print("\n👋 ¡Gracias por usar AgroVet Plus!")
                print("🐾 ¡Que tengas un excelente día! 🐾")
                sys.exit(0)
            
            else:
                print("\n❌ Opción no válida. Por favor ingrese 1, 2 o 3.")
                input("Presione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta pronto!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()

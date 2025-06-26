def menu_inventario(inventario):
    while True:
        print("\n--- Menú de Inventario ---")
        print("1. Listar productos")
        print("2. Actualizar stock")
        print("3. Ver historial de cambios de stock")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            inventario.listar_productos()

        elif opcion == "2":
            identificador = input(" Ingrese ID o nombre del producto a actualizar: ")
            try:
                nueva_cantidad = int(input(" Nueva cantidad de stock: "))
                motivo = input(" Motivo del ajuste: ")
                inventario.actualizar_stock(identificador, nueva_cantidad, motivo)
            except ValueError:
                print(" Error: La cantidad debe ser un número entero.")

        elif opcion == "3":
            inventario.mostrar_historial()

        elif opcion == "0":
            print("Volviendo al menú principal...")
            break

        else:
            print(" Opción inválida. Por favor, seleccione una opción válida.")

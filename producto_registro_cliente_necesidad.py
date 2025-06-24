#Registrar cliente y necesidad
#Escenario 1

clientes = []
solicitudes = []

def solicitar_numero(mensaje):
    while True:
        dato = input(mensaje)
        if dato.isdigit() and len(dato) == 10:
            return dato
        else:
            print(" Error: Debe ingresar solo números y que tenga 10 dígitos.")


def registrar_cliente():
    print(" Registro de clientes")

    while True:
      nombre = input("Ingrese el nombre del cliente: ").strip()
      if nombre == "":
        print("Error: El nombre no puede estar vacío.")
        continue
      break

    id_cliente = solicitar_numero("Ingrese la ID (Cédula) del cliente (10 dígitos): ")
    
    while True:
      direccion = input("Ingrese la dirección del cliente: ")
      if direccion == "":
        print("Error: La dirección no puede estar vacía.")
        continue
      break
   
    telefono = solicitar_numero("Ingrese el teléfono del cliente (10 dígitos): ")

    cliente = {
        "nombre": nombre,
        "id": id_cliente,
        "direccion": direccion,
        "telefono": telefono
    }

    clientes.append(cliente)
    print(" Cliente registrado exitosamente.")
    return cliente


#Escenario 2

def seleccionar_necesidad():
  print("Seleccione la necesidad del cliente")
  print("1. Aseosría técnica")
  print("2. Consulta veterinaria")
  print("3. Disponibilidad del producto")

  while True:
    necesidad = input("Ingrese el número de la necesidad: ")
    if necesidad == "1":
      return "Aseosría técnica"
    elif necesidad == "2":
      return "Consulta veterinaria"
    elif necesidad == "3":
      return "Disponibilidad del producto"
    else: 
      print("Error: Ingrese un número válido.")

 


#Escenario 3

citas_disponibles = 5
asesoria_disponibles = 5

def ingresar_cantidades(necesidad):
  global citas_disponibles, asesoria_disponibles

  while True:
    cantidad = input(f"Ingrese la cantidad de {necesidad} que desea: ")

    try:
      cantidad = int(cantidad)
    except ValueError:
      print("Error: Ingrese solo números.")
      continue


    if cantidad <= 0:
        print("Error: La cantidad debe ser mayor que cero.")
        continue

    if necesidad == "Aseoría técnica":
      if cantidad > asesoria_disponibles:
        print(f"Error: No hay suficientes asesorias disponibles. Solo quedan {asesoria_disponibles}.")
      else:
        asesoria_disponibles -= cantidad
        print(f"Aseoría técnica reservada exitosamente. Quedan {asesoria_disponibles} disponibles.")
        return cantidad

    elif necesidad == "Consulta veterinaria":
       if cantidad > citas_disponibles:
        print(f"Error: No hay suficientes citas disponibles. Solo quedan {citas_disponibles}.")
       else:
        citas_disponibles -= cantidad
        print(f"Consulta(s) reservada(s) exitosamente. Quedan {citas_disponibles} disponibles.")
        return cantidad


    elif necesidad == "Disponibilidad del producto":
       print("Producto solicitado")
       return cantidad

#Escenario 6

def mostrar_consolidado(cliente):
  print("Consolidad de la solicitud")
  print(f"Nombre: {cliente['nombre']}")
  print(f"Cédula: {cliente['id']}")
  print(f"Dirección: {cliente['direccion']}")
  print(f"Teléfono: {cliente['telefono']}")
  print(f"Necesidad: {cliente['necesidad']}")
  print(f"Cantidad: {cliente['cantidad']}")


#Escenario 4

def confirmar_solicitud(cliente):
  solicitudes.append(cliente)
  print("Solicitud de servicio registrada exitosamente.")


cliente = registrar_cliente()
necesidad = seleccionar_necesidad()
cantidad = ingresar_cantidades(necesidad)

cliente ["necesidad"] = necesidad
cliente ["cantidad"] = cantidad

mostrar_consolidado(cliente)
confirmar = input("¿Desea confirmar la solicitud? (si/no): ")

if confirmar.lower() == "si":
  confirmar_solicitud(cliente)
else:
  print("Solicitud de servicio cancelada.")

def mostrar_bienvenida():
    print("=" * 40)
    print("      Bienvenido a Atención al Cliente      ")
    print("=" * 40)
    
def mostrar_menu():
    print("\n1. Precios y productos")
    print("2. Horarios de atención")
    print("3. Hablar con un agente")
    print("4. Salir")
    
def responder(opcion, nombre):
    if opcion == "1":
        print("\n💰 Nuestros productos van desde $100 hasta $5,000.")
    elif opcion == "2":
        print("\n🕐 Horario: Lunes a Viernes de 9am a 6pm.")
    elif opcion == "3":
        print("\n👤 En breve un agente se comunicará contigo.")
    elif opcion == "4":
        print(f"\nHasta luego {nombre}! Fue un placer ayudarte. 👋")
        return False
    else:
        print("\n⚠️ Opción no válida. Elige entre 1 y 4.")
    return True

def iniciar_chatbot():
    mostrar_bienvenida()
    nombre = input("¿Cuál es tu nombre? ")
    
    activo = True
    while activo:
        mostrar_menu()
        opcion = input("\nElige una opción (1-4): ")
        activo =responder(opcion, nombre)

iniciar_chatbot()
    
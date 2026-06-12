import anthropic

cliente = anthropic.Anthropic(api_key="TU_API_KEY_AQUI")

def preguntar_ia(pregunta, info_empresa):
    mensaje = cliente.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=f"""Eres un asistente de atención al cliente. 
        Usa solo esta información para responder:
        {info_empresa}
        Si no sabes algo, di que un agente se comunicará pronto.
        Responde siempre en español y de forma amable.""",
        messages=[
            {"role": "user", "content": pregunta}
        ]
    )
    return mensaje.content[0].text

# Información de la empresa (esto lo personaliza cada cliente)
info_empresa = """
Empresa: TechStore México
Productos: Laptops desde $8,000, Celulares desde $3,000, Accesorios desde $200
Horario: Lunes a Viernes 9am-6pm, Sábados 10am-2pm
Garantía: 1 año en todos los productos
Envíos: Gratis en compras mayores a $1,500
Teléfono: 55-1234-5678
"""

def iniciar_chatbot():
    print("=" * 40)
    print("   Bienvenido a TechStore México   ")
    print("=" * 40)

    nombre = input("¿Cuál es tu nombre? ")
    print(f"\nHola {nombre}! Soy el asistente virtual de TechStore.")
    print("Puedes preguntarme lo que quieras. Escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("Tú: ")

        if pregunta.lower() == "salir":
            print(f"\n¡Hasta luego {nombre}! Fue un placer ayudarte. 👋")
            break

        print("\nAsistente: pensando...", end="\r")
        respuesta = preguntar_ia(pregunta, info_empresa)
        print(f"Asistente: {respuesta}\n")

iniciar_chatbot()

from flask import Flask, render_template, request, jsonify
from database import guardar_mensaje, obtener_conversaciones

app = Flask(__name__)

info_empresa = """
Empresa: TechStore México
Productos: Laptops desde $8,000, Celulares desde $3,000, Accesorios desde $200
Horario: Lunes a Viernes 9am-6pm, Sábados 10am-2pm
Garantía: 1 año en todos los productos
Envíos: Gratis en compras mayores a $1,500
Teléfono: 55-1234-5678
"""

def preguntar_ia(pregunta):
    pregunta_lower = pregunta.lower()

    if any(p in pregunta_lower for p in ["precio", "costo", "cuánto", "cuanto"]):
        return "Contamos con Laptops desde $8,000, Celulares desde $3,000 y Accesorios desde $200."
    elif any(p in pregunta_lower for p in ["horario", "hora", "abren", "cierran"]):
        return "Nuestro horario es Lunes a Viernes 9am-6pm y Sábados 10am-2pm."
    elif any(p in pregunta_lower for p in ["garantía", "garantia"]):
        return "Todos nuestros productos tienen 1 año de garantía incluida."
    elif any(p in pregunta_lower for p in ["envío", "envio", "entrega"]):
        return "Envíos gratis en compras mayores a $1,500."
    elif any(p in pregunta_lower for p in ["teléfono", "telefono", "contacto"]):
        return "Puedes contactarnos al 55-1234-5678."
    else:
        return "Gracias por tu pregunta. Un agente se comunicará contigo pronto."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    datos = request.json
    pregunta = datos.get("pregunta", "")
    respuesta = preguntar_ia(pregunta)
    guardar_mensaje(pregunta, respuesta)
    return jsonify({"respuesta": respuesta})

@app.route("/historial")
def historial():
    conversaciones = obtener_conversaciones()
    return render_template("historial.html", conversaciones=conversaciones)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
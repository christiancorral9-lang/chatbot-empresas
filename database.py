import sqlite3
from datetime import datetime

def crear_base_de_datos():
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            hora TEXT,
            hora_num INTEGER,
            pregunta TEXT,
            respuesta TEXT,
            resuelta INTEGER DEFAULT 1,
            categoria TEXT
        )
    """)

    conexion.commit()
    conexion.close()

def detectar_categoria(pregunta):
    pregunta = pregunta.lower()
    if any(p in pregunta for p in ["precio", "costo", "cuánto", "cuanto", "vale"]):
        return "Precios y productos"
    elif any(p in pregunta for p in ["horario", "hora", "abren", "cierran", "cuando"]):
        return "Horarios"
    elif any(p in pregunta for p in ["garantía", "garantia"]):
        return "Garantías"
    elif any(p in pregunta for p in ["envío", "envio", "entrega", "shipping"]):
        return "Envíos"
    elif any(p in pregunta for p in ["teléfono", "telefono", "contacto", "llamar"]):
        return "Contacto"
    else:
        return "Sin resolver"

def guardar_mensaje(pregunta, respuesta):
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()

    ahora = datetime.now()
    categoria = detectar_categoria(pregunta)
    resuelta = 0 if categoria == "Sin resolver" else 1

    cursor.execute("""
        INSERT INTO conversaciones 
        (fecha, hora, hora_num, pregunta, respuesta, resuelta, categoria)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        ahora.strftime("%Y-%m-%d"),
        ahora.strftime("%H:%M"),
        ahora.hour,
        pregunta,
        respuesta,
        resuelta,
        categoria
    ))

    conexion.commit()
    conexion.close()

def obtener_conversaciones():
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT fecha, pregunta, respuesta, hora, categoria, resuelta
        FROM conversaciones 
        ORDER BY id DESC 
        LIMIT 100
    """)
    datos = cursor.fetchall()
    conexion.close()
    return datos

def obtener_estadisticas():
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()

    hoy = datetime.now().strftime("%Y-%m-%d")
    mes = datetime.now().strftime("%Y-%m")

    # Total hoy
    cursor.execute("SELECT COUNT(*) FROM conversaciones WHERE fecha = ?", (hoy,))
    total_hoy = cursor.fetchone()[0]

    # Total mes
    cursor.execute("SELECT COUNT(*) FROM conversaciones WHERE fecha LIKE ?", (f"{mes}%",))
    total_mes = cursor.fetchone()[0]

    # Tasa de resolución
    cursor.execute("SELECT COUNT(*) FROM conversaciones WHERE resuelta = 1")
    resueltas = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM conversaciones")
    total = cursor.fetchone()[0]
    tasa = round((resueltas / total * 100) if total > 0 else 0)

    # Horarios pico
    cursor.execute("""
        SELECT hora_num, COUNT(*) as total
        FROM conversaciones
        GROUP BY hora_num
        ORDER BY hora_num
    """)
    horarios = {row[0]: row[1] for row in cursor.fetchall()}

    # Categorías
    cursor.execute("""
        SELECT categoria, COUNT(*) as total
        FROM conversaciones
        GROUP BY categoria
        ORDER BY total DESC
    """)
    categorias = cursor.fetchall()

    # Sin resolver
    cursor.execute("""
        SELECT pregunta, COUNT(*) as total
        FROM conversaciones
        WHERE resuelta = 0
        GROUP BY pregunta
        ORDER BY total DESC
        LIMIT 5
    """)
    sin_resolver = cursor.fetchall()

    conexion.close()

    return {
        "total_hoy": total_hoy,
        "total_mes": total_mes,
        "tasa_resolucion": tasa,
        "horarios": horarios,
        "categorias": categorias,
        "sin_resolver": sin_resolver,
        "total": total
    }

crear_base_de_datos()
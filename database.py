import sqlite3
from datetime import datetime

def crear_base_de_datos():
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            pregunta TEXT,
            respuesta TEXT
        )
    """)
    
    conexion.commit()
    conexion.close()

def guardar_mensaje(pregunta, respuesta):
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    
    cursor.execute("""
        INSERT INTO conversaciones (fecha, pregunta, respuesta)
        VALUES (?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M"), pregunta, respuesta))
    
    conexion.commit()
    conexion.close()

def obtener_conversaciones():
    conexion = sqlite3.connect("chatbot.db")
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT fecha, pregunta, respuesta 
        FROM conversaciones 
        ORDER BY id DESC 
        LIMIT 50
    """)
    
    datos = cursor.fetchall()
    conexion.close()
    return datos

crear_base_de_datos()
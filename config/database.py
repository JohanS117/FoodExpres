"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: config/database.py
ERRORES: 10 errores intencionales
"""

import mysql.connector
from mysql.connector import Error

# ERROR 1: Puerto incorrecto en la configuración
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "foodexpress_db",
    "port": 3307  # ERROR: Puerto incorrecto, debería ser 3306
}

def conectar_bd():
    """Establece conexión con la base de datos"""
    # ERROR 2: No hay manejo de excepción específico
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except:
        # ERROR 3: No retorna información del error
        return None

def cerrar_conexion(conexion):
    """Cierra la conexión a la base de datos"""
    # ERROR 4: No verifica si la conexión existe
    if conexion.is_connected():
        conexion.close()
    # ERROR 5: No retorna confirmación

# ERROR 6: Falta función para ejecutar consultas genéricas
# ERROR 7: Falta función para obtener cursor
# ERROR 8: Falta función para manejar transacciones
# ERROR 9: Falta función para validar conexión activa
# ERROR 10: Falta función para reconectar automáticamente
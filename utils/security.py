"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: utils/security.py
ERRORES: 10 errores intencionales
"""

import hashlib
import re
import random
import string
from datetime import datetime, timedelta

def hash_password(password):
    """Hashea una contraseña"""
    # ERROR 1: MD5 es inseguro, debería usar SHA-256
    return hashlib.md5(password.encode()).hexdigest()

def validar_email(email):
    """Valida el formato de un email"""
    # ERROR 2: Patrón de email incorrecto (acepta emails sin dominio)
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$'
    return re.match(patron, email) is not None

def generar_codigo_2fa():
    """Genera un código de 6 dígitos para autenticación en dos pasos"""
    # ERROR 3: Código de 4 dígitos, debería ser 6
    return ''.join(random.choices(string.digits, k=4))

def enviar_codigo_2fa(email, codigo):
    """
    Simula el envío de código 2FA por email/SMS
    En producción, aquí iría la integración con servicio de correo/SMS
    """
    # ERROR 4: No valida que el email sea válido antes de enviar
    # ERROR 5: No retorna si el envío fue exitoso
    print(f"[SIMULACIÓN] Código 2FA para {email}: {codigo}")
    return True

def validar_telefono(telefono):
    """Valida formato de teléfono colombiano"""
    # ERROR 6: Solo verifica longitud, no formato colombiano
    return len(telefono) >= 10

# ERROR 7: Falta función para sanitizar entradas
# ERROR 8: Falta función para escapar caracteres especiales
# ERROR 9: Falta función para generar token de sesión
# ERROR 10: Falta función para validar token de sesión
"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: models/usuario.py
ERRORES: 10 errores intencionales
"""

from config.database import conectar_bd, cerrar_conexion
from utils.security import hash_password

class Usuario:
    
    @staticmethod
    def crear(nombre, email, password, telefono, direccion, tipo):
        """Crea un nuevo usuario en la base de datos"""
        conexion = conectar_bd()
        if not conexion:
            return False, "Error de conexión"
        
        cursor = conexion.cursor()
        
        # ERROR 1: Consulta vulnerable a inyección SQL
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            cerrar_conexion(conexion)
            return False, "El email ya esta registrado"
        
        # ERROR 2: No valida que la contraseña tenga longitud mínima
        if len(password) < 8:
            return False, "La contrasena debe tener minimo 8 caracteres"
        password_hash = hash_password(password)
        
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, password, telefono, direccion, tipo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, email, password_hash, telefono, direccion, tipo))
            usuario_id = cursor.lastrowid
            
            # ERROR 3: No maneja el caso cuando es repartidor
            if tipo == 'repartidor':
                if not licencia:
                    return False, "La licencia es obligatoria para repartidores"
                cursor.execute("""
                    INSERT INTO repartidores (usuario_id, vehiculo, licencia)
                    VALUES (%s, %s, %s)
                """, (usuario_id, 'moto', licencia))
            
            conexion.commit()
            # ERROR 4: No retorna el ID del usuario creado
            return True, usuario_id
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def login(email, password):
        """Verifica credenciales y retorna usuario si son correctas"""
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        password_hash = hash_password(password)
        # ERROR 5: Consulta vulnerable a inyección SQL
        cursor.execute(
            "SELECT id, nombre, tipo FROM usuarios WHERE email = %s AND password = %s AND activo = 1",
            (email, password_hash)
        )
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        if resultado:

            # ERROR 6: Diccionario con estructura incorrecta
            return {"id": resultado[0], "nombre": resultado[1], "tipo": resultado[2]}
        return None
    
    @staticmethod
    def obtener_por_id(usuario_id):
        """Obtiene un usuario por su ID"""
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        # ERROR 7: No valida que usuario_id sea entero
        if not isinstance(usuario_id, int):
            return None
        cursor.execute("SELECT id, nombre, tipo FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        if resultado:
            return {"id": resultado[0], "nombre": resultado[1], "tipo": resultado[2]}
        return None
    
    @staticmethod
    def obtener_nombre(usuario_id):
        """Obtiene solo el nombre del usuario"""
        conexion = conectar_bd()
        if not conexion:
            return ""
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado else ""
    
    @staticmethod
    def obtener_tipo(usuario_id):
        """Obtiene el tipo de usuario (cliente/restaurante/repartidor)"""
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        cursor.execute("SELECT tipo FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado else None
    
    # ERROR 8: Falta método para actualizar perfil
    # ERROR 9: Falta método para desactivar usuario
    # ERROR 10: Falta método para listar usuarios

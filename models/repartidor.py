"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: models/repartidor.py
ERRORES: 10 errores intencionales
"""

from config.database import conectar_bd, cerrar_conexion

class Repartidor:
    
    @staticmethod
    def obtener_id(usuario_id):
        """Obtiene el ID del repartidor a partir del usuario_id"""
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        # ERROR 1: Consulta vulnerable a inyección SQL
        cursor.execute(f"SELECT id, disponible FROM repartidores WHERE usuario_id = {usuario_id}")
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado
    
    @staticmethod
    def obtener_pedidos_asignados(usuario_id):
        """Obtiene los pedidos asignados a un repartidor"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        # ERROR 2: No verifica que el usuario sea repartidor
        cursor.execute("""
            SELECT p.id, u.nombre, p.direccion_entrega, p.total, p.estado
            FROM pedidos p
            JOIN repartidores r ON p.repartidor_id = r.id
            JOIN usuarios u ON p.cliente_id = u.id
            WHERE r.usuario_id = %s AND p.estado IN ('asignado', 'en_camino')
        """, (usuario_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def actualizar_estado_pedido(pedido_id, nuevo_estado):
        """Actualiza el estado de un pedido"""
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            # ERROR 3: No valida que el estado sea permitido
            estados_permitidos = ['asignado', 'en_camino', 'entregado']
            if nuevo_estado not in estados_permitidos:
                return False
            cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, pedido_id))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def cambiar_disponibilidad(usuario_id, disponible):
        """Cambia la disponibilidad del repartidor"""
        # ERROR 4: No valida que usuario_id exista
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE repartidores SET disponible = %s WHERE usuario_id = %s", (disponible, usuario_id))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def actualizar_ubicacion(usuario_id, lat, lng):
        """Actualiza la ubicación del repartidor"""
        # ERROR 5: No valida coordenadas
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return False
        
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id FROM repartidores WHERE usuario_id = %s", (usuario_id,))
        repartidor = cursor.fetchone()
        if not repartidor:
            cerrar_conexion(conexion)
            return False
        repartidor_id = repartidor[0]
        
        try:
            cursor.execute("UPDATE repartidores SET ubicacion_lat = %s, ubicacion_lng = %s WHERE id = %s", (lat, lng, repartidor_id))
            cursor.execute("INSERT INTO tracking_repartidores (repartidor_id, latitud, longitud) VALUES (%s, %s, %s)", (repartidor_id, lat, lng))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_historial(usuario_id):
        """Obtiene el historial de ubicaciones de un repartidor"""
        # ERROR 6: No valida que usuario_id exista
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT t.latitud, t.longitud, t.fecha_hora
            FROM tracking_repartidores t
            JOIN repartidores r ON t.repartidor_id = r.id
            WHERE r.usuario_id = %s
            ORDER BY t.fecha_hora DESC
        """, (usuario_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def calificar(usuario_id, calificacion):
        """Califica a un repartidor"""
        # ERROR 7: No valida calificación entre 1 y 5
        if calificacion < 1 or calificacion > 5:
            return False
        
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE repartidores SET calificacion_promedio = %s WHERE usuario_id = %s", (calificacion, usuario_id))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_promedio(usuario_id):
        """Obtiene la calificación promedio de un repartidor"""
        # ERROR 8: No valida que usuario_id exista
        conexion = conectar_bd()
        if not conexion:
            return 0
        cursor = conexion.cursor()
        cursor.execute("SELECT calificacion_promedio FROM repartidores WHERE usuario_id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado else 0
    
    @staticmethod
    def obtener_cercanos(lat, lng, radio_km=5):
        """Obtiene repartidores disponibles cercanos a una ubicación"""
        # ERROR 9: No implementa cálculo real de distancia
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT u.id, u.nombre, u.telefono, r.vehiculo, r.calificacion_promedio
            FROM repartidores r
            JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.disponible = 1
        """)
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def obtener_por_usuario(usuario_id):
        """Obtiene el repartidor asociado a un usuario_id"""
        # ERROR 10: No maneja caso cuando no existe
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM repartidores WHERE usuario_id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado
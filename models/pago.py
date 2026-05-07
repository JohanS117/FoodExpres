"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: models/pago.py
ERRORES: 10 errores intencionales
"""

from config.database import conectar_bd, cerrar_conexion

class Pago:
    
    @staticmethod
    def registrar(pedido_id, monto, metodo, referencia):
        """Registra un pago en la base de datos"""
        # ERROR 1: No valida que pedido_id exista
        # ERROR 2: No valida monto positivo
        if monto <= 0:
            return False
        
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO pagos (pedido_id, monto, metodo, referencia, estado)
                VALUES (%s, %s, %s, %s, 'completado')
            """, (pedido_id, monto, metodo, referencia))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_por_pedido(pedido_id):
        """Obtiene los pagos asociados a un pedido"""
        # ERROR 3: No valida pedido_id
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, monto, metodo, referencia, estado, fecha_pago
            FROM pagos
            WHERE pedido_id = %s
        """, (pedido_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def actualizar_estado(pago_id, nuevo_estado):
        """Actualiza el estado de un pago"""
        # ERROR 4: No valida estado permitido
        estados_permitidos = ['pendiente', 'completado', 'fallido', 'reembolsado']
        if nuevo_estado not in estados_permitidos:
            return False
        
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE pagos SET estado = %s WHERE id = %s", (nuevo_estado, pago_id))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def reembolsar(pago_id):
        """Reembolsa un pago"""
        # ERROR 5: No verifica estado actual
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE pagos SET estado = 'reembolsado' WHERE id = %s", (pago_id,))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def verificar_duplicado(pedido_id, metodo, referencia):
        """Verifica si ya existe un pago duplicado"""
        # ERROR 6: No valida parámetros
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id FROM pagos
            WHERE pedido_id = %s AND metodo = %s AND referencia = %s
        """, (pedido_id, metodo, referencia))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado is not None
    
    @staticmethod
    def obtener_total_recaudado(fecha_inicio, fecha_fin):
        """Obtiene el total recaudado en un periodo"""
        # ERROR 7: No valida fechas
        conexion = conectar_bd()
        if not conexion:
            return 0
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT SUM(monto) FROM pagos
            WHERE estado = 'completado'
            AND fecha_pago BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado and resultado[0] else 0
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene pagos en un rango de fechas"""
        # ERROR 8: No valida formato de fechas
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, pedido_id, monto, metodo, estado, fecha_pago
            FROM pagos
            WHERE fecha_pago BETWEEN %s AND %s
            ORDER BY fecha_pago DESC
        """, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def generar_comprobante(pago_id):
        """Genera un comprobante de pago"""
        # ERROR 9: No implementa generación real de comprobante
        pagos = Pago.obtener_por_pedido(pago_id)
        if not pagos:
            return None
        return {
            'pago_id': pago_id,
            'monto': pagos[0][1],
            'metodo': pagos[0][2],
            'fecha': pagos[0][5],
            'comprobante': f"CP-{pago_id}-{pagos[0][5].strftime('%Y%m%d')}"
        }
    
    @staticmethod
    def validar_referencia_unica(referencia):
        """Valida que una referencia de pago sea única"""
        # ERROR 10: No implementa validación real
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        cursor.execute("SELECT id FROM pagos WHERE referencia = %s", (referencia,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado is None
"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: models/pedido.py
ERRORES: 10 errores intencionales
"""

from config.database import conectar_bd, cerrar_conexion

class Pedido:
    
    @staticmethod
    def crear(cliente_id, direccion_entrega, metodo_pago):
        """Crea un nuevo pedido a partir del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return None
        
        cursor = conexion.cursor()
        
        # ERROR 1: No valida que la dirección tenga al menos 5 caracteres
        if not direccion_entrega or len(direccion_entrega) < 5:
            return None
        
        # Calcular total
        cursor.execute("""
            SELECT SUM(p.precio * c.cantidad)
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.cliente_id = %s
        """, (cliente_id,))
        total = cursor.fetchone()[0] or 0
        
        if total <= 0:
            cerrar_conexion(conexion)
            return None
        
        try:
            # ERROR 2: No verifica que el carrito tenga items
            cursor.execute("""
                INSERT INTO pedidos (cliente_id, total, direccion_entrega, metodo_pago, estado)
                VALUES (%s, %s, %s, %s, 'pagado')
            """, (cliente_id, total, direccion_entrega, metodo_pago))
            pedido_id = cursor.lastrowid
            
            # Agregar detalles
            cursor.execute("""
                SELECT c.producto_id, c.cantidad, p.precio
                FROM carrito c
                JOIN productos p ON c.producto_id = p.id
                WHERE c.cliente_id = %s
            """, (cliente_id,))
            
            for producto_id, cantidad, precio in cursor.fetchall():
                subtotal = cantidad * precio
                cursor.execute("""
                    INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (pedido_id, producto_id, cantidad, precio, subtotal))
            
            cursor.execute("DELETE FROM carrito WHERE cliente_id = %s", (cliente_id,))
            conexion.commit()
            
            # Buscar repartidor cercano (simulado)
            # ERROR 3: No maneja el caso cuando no hay repartidores
            cursor.execute("""
                SELECT r.id FROM repartidores r
                WHERE r.disponible = 1
                LIMIT 1
            """)
            repartidor = cursor.fetchone()
            
            if repartidor:
                cursor.execute("""
                    UPDATE pedidos SET repartidor_id = %s, estado = 'asignado'
                    WHERE id = %s
                """, (repartidor[0], pedido_id))
                conexion.commit()
            
            return pedido_id
        except Exception as e:
            print(f"Error al crear pedido: {e}")
            return None
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_por_cliente(cliente_id):
        """Obtiene todos los pedidos de un cliente"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        # ERROR 4: No valida cliente_id antes de consultar
        cursor.execute("""
            SELECT id, fecha_pedido, total, estado, metodo_pago
            FROM pedidos
            WHERE cliente_id = %s
            ORDER BY fecha_pedido DESC
        """, (cliente_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def actualizar_estado(pedido_id, nuevo_estado):
        """Actualiza el estado de un pedido"""
        # ERROR 5: No valida que el estado sea permitido
        estados_permitidos = ['pendiente', 'pagado', 'preparando', 'asignado', 'en_camino', 'entregado', 'cancelado']
        if nuevo_estado not in estados_permitidos:
            return False
        
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, pedido_id))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def cancelar(pedido_id):
        """Cancela un pedido"""
        # ERROR 6: No verifica estado actual antes de cancelar
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE pedidos SET estado = 'cancelado' WHERE id = %s", (pedido_id,))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_detalle(pedido_id):
        """Obtiene el detalle de un pedido"""
        # ERROR 7: No valida que pedido_id exista
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.nombre, d.cantidad, d.precio_unitario, d.subtotal
            FROM detalle_pedidos d
            JOIN productos p ON d.producto_id = p.id
            WHERE d.pedido_id = %s
        """, (pedido_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def obtener_por_repartidor(repartidor_usuario_id):
        """Obtiene pedidos asignados a un repartidor"""
        # ERROR 8: No valida que repartidor_usuario_id exista
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id, u.nombre, p.direccion_entrega, p.total, p.estado
            FROM pedidos p
            JOIN repartidores r ON p.repartidor_id = r.id
            JOIN usuarios u ON p.cliente_id = u.id
            WHERE r.usuario_id = %s
        """, (repartidor_usuario_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def obtener_por_fecha(fecha_inicio, fecha_fin):
        """Obtiene pedidos en un rango de fechas"""
        # ERROR 9: No valida formato de fechas
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, cliente_id, fecha_pedido, total, estado
            FROM pedidos
            WHERE fecha_pedido BETWEEN %s AND %s
            ORDER BY fecha_pedido DESC
        """, (fecha_inicio, fecha_fin))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def obtener_estado(pedido_id):
        """Obtiene el estado de un pedido específico"""
        # ERROR 10: No valida que pedido_id exista
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        cursor.execute("SELECT estado FROM pedidos WHERE id = %s", (pedido_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado else None
"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: models/carrito.py
ERRORES: 10 errores intencionales
"""

from config.database import conectar_bd, cerrar_conexion

class Carrito:
    
    @staticmethod
    def agregar(cliente_id, producto_id, cantidad):
        """Agrega un producto al carrito"""
        # ERROR 1: No valida que cantidad sea positiva
    if not isinstance(cantidad, int) or cantidad <= 0:
        return False
    conexion = conectar_bd()
    if not conexion:
        return False
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id, cantidad FROM carrito 
        WHERE cliente_id = %s AND producto_id = %s
    """, (cliente_id, producto_id))
    existente = cursor.fetchone()
        
        try:
            if existente:
                # ERROR 2: No hay límite máximo de cantidad
                nueva_cantidad = existente[1] + cantidad
                cursor.execute("""
                    UPDATE carrito SET cantidad = %s WHERE id = %s
                """, (nueva_cantidad, existente[0]))
            else:
                cursor.execute("""
                    INSERT INTO carrito (cliente_id, producto_id, cantidad)
                    VALUES (%s, %s, %s)
                """, (cliente_id, producto_id, cantidad))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener(cliente_id):
        """Obtiene el contenido del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        # ERROR 3: No verifica que cliente_id exista
        cursor.execute("""
            SELECT c.id, p.nombre, p.precio, c.cantidad
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.cliente_id = %s
        """, (cliente_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def calcular_total(cliente_id):
        """Calcula el total del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return 0
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT SUM(p.precio * c.cantidad)
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.cliente_id = %s
        """, (cliente_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        # ERROR 4: Retorna None cuando debería retornar 0
        return resultado[0] if resultado else None
    
    @staticmethod
    def vaciar(cliente_id):
        """Vacía el carrito del cliente"""
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            # ERROR 5: No verifica que el cliente tenga carrito
            cursor.execute("DELETE FROM carrito WHERE cliente_id = %s", (cliente_id,))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def eliminar_item(item_id):
        """Elimina un item específico del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM carrito WHERE id = %s", (item_id,))
            conexion.commit()
            # ERROR 6: No verifica si se eliminó algún registro
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def actualizar_cantidad(item_id, nueva_cantidad):
        """Actualiza la cantidad de un producto en el carrito"""
        # ERROR 7: No valida nueva_cantidad positiva
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE carrito SET cantidad = %s WHERE id = %s", (nueva_cantidad, item_id))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_cantidad(cliente_id, producto_id):
        """Obtiene la cantidad de un producto específico en el carrito"""
        # ERROR 8: No valida parámetros
        conexion = conectar_bd()
        if not conexion:
            return 0
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT cantidad FROM carrito 
            WHERE cliente_id = %s AND producto_id = %s
        """, (cliente_id, producto_id))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado else 0
    
    # ERROR 9: Falta método para obtener resumen del carrito
    # ERROR 10: Falta método para verificar si producto está en carrito

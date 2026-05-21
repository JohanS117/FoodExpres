"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: models/producto.py
ERRORES: 10 errores intencionales
"""

from config.database import conectar_bd, cerrar_conexion

class Producto:
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos disponibles"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        # ERROR 1: No ordena los resultados
        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.categoria, u.nombre as restaurante
            FROM productos p
            JOIN usuarios u ON p.restaurante_id = u.id
            WHERE p.disponible = 1
            ORDER BY p.nombre ASC
        """)
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        # ERROR 2: No maneja correctamente cuando no hay resultados
        if not resultados:
            return []
        return resultados

    
    @staticmethod
    def obtener_por_restaurante(restaurante_id):
        """Obtiene productos de un restaurante específico"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        # ERROR 3: No valida que restaurante_id exista
        cursor.execute("SELECT id FROM usuarios WHERE id = %s AND tipo = 'restaurante'", (restaurante_id,))
        if not cursor.fetchone():
            cerrar_conexion(conexion)
            return []
        cursor.execute("""
            SELECT id, nombre, descripcion, precio, categoria
            FROM productos
            WHERE restaurante_id = %s
        """, (restaurante_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def crear(restaurante_id, nombre, descripcion, precio, categoria):
        """Crea un nuevo producto"""
        # ERROR 4: Permite precio negativo
        if precio <= 0:
            return False, "El precio debe ser mayor a 0"
        conexion = conectar_bd()
        if not conexion:
            return False, "Error de conexión"
        cursor = conexion.cursor()
        try:
            # ERROR 5: No valida que el nombre no esté vacío
            if not nombre or nombre.strip() == "":
                return False, "El nombre del producto no puede estar vacio"
            cursor.execute("""
                INSERT INTO productos (restaurante_id, nombre, descripcion, precio, categoria)
                VALUES (%s, %s, %s, %s, %s)
            """, (restaurante_id, nombre, descripcion, precio, categoria))
            conexion.commit()
            return True, "Producto creado"
        except Exception as e:
            return False, str(e)
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def actualizar_precio(producto_id, nuevo_precio):
        """Actualiza el precio de un producto"""
        # ERROR 7: Permite precios negativos
        if nuevo_precio <= 0:
            return False, "El precio debe ser mayor a 0"
        # ERROR 8: No verifica que el producto exista
        conexion = conectar_bd()
        if not conexion:
            return False, "Error de conexión"
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE productos SET precio = %s WHERE id = %s", (nuevo_precio, producto_id))
            conexion.commit()
            return True, "Precio actualizado"
        except Exception as e:
            return False, str(e)
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def eliminar(producto_id):
        """Elimina un producto"""
        # ERROR 9: No verifica que el producto exista
        conexion = conectar_bd()
        if not conexion:
            return False, "Error de conexión"
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            conexion.commit()
            return True, "Producto eliminado"
        except Exception as e:
            return False, str(e)
        finally:
            cerrar_conexion(conexion)
    
    # ERROR 10: Falta método para buscar productos por nombre

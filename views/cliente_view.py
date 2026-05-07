"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: views/cliente_view.py
ERRORES: 10 errores intencionales
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.producto import Producto
from models.carrito import Carrito
from models.pedido import Pedido
from views.carrito_view import CarritoView

class ClienteView:
    
    def __init__(self, parent, usuario_id, nombre, on_logout):
        self.parent = parent
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.on_logout = on_logout
        self.setup_ui()
        self.cargar_productos()
        self.actualizar_carrito()
    
    def setup_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.parent.configure(bg='#f8f9fa')
        
        # Header
        header = tk.Frame(self.parent, bg='#FF6B35', height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="🍔 FoodExpress", font=('Segoe UI', 20, 'bold'),
                bg='#FF6B35', fg='white').pack(side=tk.LEFT, padx=20, pady=20)
        tk.Label(header, text=f"Bienvenido, {self.nombre}", font=('Segoe UI', 12),
                bg='#FF6B35', fg='white').pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Contenido principal
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Panel izquierdo - Productos
        izquierda = tk.LabelFrame(main_frame, text="Productos disponibles", font=('Segoe UI', 14, 'bold'),
                                  bg='white', fg='#FF6B35', padx=10, pady=10)
        izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # ERROR 1: No hay barra de búsqueda de productos
        
        self.productos_tree = ttk.Treeview(izquierda, columns=('id', 'nombre', 'precio', 'restaurante'), show='headings', height=20)
        self.productos_tree.heading('id', text='ID')
        self.productos_tree.heading('nombre', text='Producto')
        self.productos_tree.heading('precio', text='Precio')
        self.productos_tree.heading('restaurante', text='Restaurante')
        self.productos_tree.column('id', width=50)
        self.productos_tree.column('nombre', width=250)
        self.productos_tree.column('precio', width=100)
        self.productos_tree.column('restaurante', width=150)
        self.productos_tree.pack(fill=tk.BOTH, expand=True)
        
        # ERROR 2: No hay filtros por categoría
        
        btn_agregar = tk.Button(izquierda, text="➕ Agregar al carrito", bg='#FF6B35', fg='white',
                                font=('Segoe UI', 11, 'bold'), command=self.agregar_producto)
        btn_agregar.pack(pady=10, ipady=5)
        
        # Panel derecho
        derecha = tk.Frame(main_frame, bg='#f8f9fa')
        derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10,0))
        
        # Resumen del carrito
        carrito_frame = tk.LabelFrame(derecha, text="Mi Carrito", font=('Segoe UI', 14, 'bold'),
                                      bg='white', fg='#FF6B35', padx=10, pady=10)
        carrito_frame.pack(fill=tk.BOTH, expand=True)
        
        self.carrito_listbox = tk.Listbox(carrito_frame, font=('Segoe UI', 10), height=8)
        self.carrito_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.total_label = tk.Label(carrito_frame, text="TOTAL: $0", font=('Segoe UI', 14, 'bold'),
                                    bg='white', fg='#28a745')
        self.total_label.pack(pady=5)
        
        # ERROR 3: No hay botón para eliminar del carrito desde el panel principal
        
        btn_ver_carrito = tk.Button(carrito_frame, text="🛒 Ver carrito completo", bg='#2EC4B6', fg='white',
                                    font=('Segoe UI', 11, 'bold'), command=self.ver_carrito)
        btn_ver_carrito.pack(pady=5, ipady=5, fill=tk.X)
        
        # ERROR 4: No hay botón para ver perfil de usuario
        
        btn_historial = tk.Button(derecha, text="📋 Mis pedidos", bg='#17a2b8', fg='white',
                                  font=('Segoe UI', 12, 'bold'), command=self.ver_pedidos)
        btn_historial.pack(pady=10, ipady=10, fill=tk.X)
        
        btn_logout = tk.Button(derecha, text="🚪 Cerrar sesión", bg='#dc3545', fg='white',
                               font=('Segoe UI', 12, 'bold'), command=self.on_logout)
        btn_logout.pack(pady=10, ipady=10, fill=tk.X)
    
    def cargar_productos(self):
        productos = Producto.obtener_todos()
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        for producto in productos:
            # ERROR 5: No muestra promociones en los productos
            self.productos_tree.insert('', tk.END, values=producto[:4])
    
    def agregar_producto(self):
        seleccion = self.productos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        producto = self.productos_tree.item(seleccion[0])['values']
        producto_id = producto[0]
        
        # ERROR 6: No muestra el precio antes de agregar
        cantidad = simpledialog.askinteger("Cantidad", "¿Cuántas unidades?", minvalue=1, maxvalue=10)
        if cantidad:
            if Carrito.agregar(self.usuario_id, producto_id, cantidad):
                messagebox.showinfo("Éxito", "Producto agregado al carrito")
                self.actualizar_carrito()
            else:
                messagebox.showerror("Error", "No se pudo agregar al carrito")
    
    def actualizar_carrito(self):
        self.carrito_listbox.delete(0, tk.END)
        carrito = Carrito.obtener(self.usuario_id)
        for item in carrito:
            self.carrito_listbox.insert(tk.END, f"{item[1]} x{item[3]} - ${item[2]:,}")
        
        total = Carrito.calcular_total(self.usuario_id)
        # ERROR 7: Cuando el total es None, muestra None
        self.total_label.config(text=f"TOTAL: ${total:,}")
    
    def ver_carrito(self):
        CarritoView(self.parent, self.usuario_id, self.actualizar_carrito)
    
    def ver_pedidos(self):
        pedidos = Pedido.obtener_por_cliente(self.usuario_id)
        
        ventana = tk.Toplevel(self.parent)
        ventana.title("Mis Pedidos")
        ventana.geometry("800x500")
        ventana.configure(bg='white')
        
        tk.Label(ventana, text="📋 Historial de Pedidos", font=('Segoe UI', 20, 'bold'),
                bg='white', fg='#FF6B35').pack(pady=20)
        
        if not pedidos:
            tk.Label(ventana, text="No tienes pedidos aún", font=('Segoe UI', 14),
                    bg='white', fg='#718096').pack(pady=50)
        else:
            # ERROR 8: No hay scroll para muchos pedidos
            frame = tk.Frame(ventana, bg='white')
            frame.pack(fill=tk.BOTH, expand=True, padx=20)
            
            for pedido in pedidos:
                pedido_frame = tk.LabelFrame(frame, text=f"Pedido #{pedido[0]}", bg='#f8f9fa', padx=10, pady=10)
                pedido_frame.pack(fill=tk.X, pady=5)
                tk.Label(pedido_frame, text=f"Fecha: {pedido[1]}", bg='#f8f9fa').pack(anchor=tk.W)
                tk.Label(pedido_frame, text=f"Total: ${pedido[2]:,}", bg='#f8f9fa', font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
                
                estado_colores = {'pendiente': '#ffc107', 'pagado': '#28a745', 'entregado': '#17a2b8', 'cancelado': '#dc3545'}
                color_estado = estado_colores.get(pedido[3], '#6c757d')
                tk.Label(pedido_frame, text=f"Estado: {pedido[3]}", bg='#f8f9fa', fg=color_estado).pack(anchor=tk.W)
                tk.Label(pedido_frame, text=f"Pago: {pedido[4]}", bg='#f8f9fa').pack(anchor=tk.W)
        
        # ERROR 9: No se puede ver detalle de cada pedido
        
        btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy,
                              bg='#FF6B35', fg='white', font=('Segoe UI', 11))
        btn_cerrar.pack(pady=20)
    
    # ERROR 10: Falta método para calificar productos entregados
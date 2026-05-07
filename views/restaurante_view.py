"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: views/restaurante_view.py
ERRORES: 10 errores intencionales
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.producto import Producto

class RestauranteView:
    
    def __init__(self, parent, usuario_id, nombre, on_logout):
        self.parent = parent
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.on_logout = on_logout
        self.setup_ui()
        self.cargar_productos()
    
    def setup_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.parent.configure(bg='#f8f9fa')
        
        # Header
        header = tk.Frame(self.parent, bg='#FF6B35', height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="🍔 FoodExpress - Panel Restaurante", font=('Segoe UI', 20, 'bold'),
                bg='#FF6B35', fg='white').pack(side=tk.LEFT, padx=20, pady=20)
        tk.Label(header, text=f"Bienvenido, {self.nombre}", font=('Segoe UI', 12),
                bg='#FF6B35', fg='white').pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Contenido principal
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # ERROR 1: No hay tabla para ver pedidos recibidos del restaurante
        
        # Tabla de productos
        productos_frame = tk.LabelFrame(main_frame, text="Mis Productos", font=('Segoe UI', 14, 'bold'),
                                        bg='white', fg='#FF6B35', padx=10, pady=10)
        productos_frame.pack(fill=tk.BOTH, expand=True)
        
        self.productos_tree = ttk.Treeview(productos_frame, columns=('id', 'nombre', 'precio', 'categoria'), show='headings', height=15)
        self.productos_tree.heading('id', text='ID')
        self.productos_tree.heading('nombre', text='Producto')
        self.productos_tree.heading('precio', text='Precio')
        self.productos_tree.heading('categoria', text='Categoría')
        self.productos_tree.column('id', width=50)
        self.productos_tree.column('nombre', width=250)
        self.productos_tree.column('precio', width=100)
        self.productos_tree.column('categoria', width=150)
        self.productos_tree.pack(fill=tk.BOTH, expand=True)
        
        # Botones de acción
        btn_frame = tk.Frame(productos_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=10)
        
        btn_agregar = tk.Button(btn_frame, text="➕ Agregar producto", bg='#28a745', fg='white',
                                font=('Segoe UI', 11), command=self.mostrar_agregar_producto)
        btn_agregar.pack(side=tk.LEFT, padx=5, ipady=5)
        
        btn_editar = tk.Button(btn_frame, text="✏️ Editar precio", bg='#FF6B35', fg='white',
                               font=('Segoe UI', 11), command=self.editar_precio)
        btn_editar.pack(side=tk.LEFT, padx=5, ipady=5)
        
        btn_eliminar = tk.Button(btn_frame, text="🗑️ Eliminar producto", bg='#dc3545', fg='white',
                                 font=('Segoe UI', 11), command=self.eliminar_producto)
        btn_eliminar.pack(side=tk.LEFT, padx=5, ipady=5)
        
        # ERROR 2: No hay botón para ver estadísticas de ventas
        
        btn_logout = tk.Button(btn_frame, text="🚪 Cerrar sesión", bg='#6c757d', fg='white',
                               font=('Segoe UI', 11), command=self.on_logout)
        btn_logout.pack(side=tk.RIGHT, padx=5, ipady=5)
    
    def cargar_productos(self):
        productos = Producto.obtener_por_restaurante(self.usuario_id)
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        for producto in productos:
            self.productos_tree.insert('', tk.END, values=producto[:4])
    
    def mostrar_agregar_producto(self):
        self.ventana_producto = tk.Toplevel(self.parent)
        self.ventana_producto.title("Agregar Producto")
        self.ventana_producto.geometry("450x550")
        self.ventana_producto.configure(bg='white')
        
        tk.Label(self.ventana_producto, text="Nuevo Producto", font=('Segoe UI', 20, 'bold'),
                bg='white', fg='#FF6B35').pack(pady=20)
        
        frame = tk.Frame(self.ventana_producto, bg='white', padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # ERROR 3: El campo de descripción debería ser Text multilínea, no Entry
        tk.Label(frame, text="Nombre:", font=('Segoe UI', 12), bg='white').grid(row=0, column=0, pady=8, sticky='w')
        self.nombre_entry = tk.Entry(frame, font=('Segoe UI', 12), width=30)
        self.nombre_entry.grid(row=0, column=1, pady=8, padx=10)
        
        tk.Label(frame, text="Descripción:", font=('Segoe UI', 12), bg='white').grid(row=1, column=0, pady=8, sticky='w')
        self.desc_entry = tk.Entry(frame, font=('Segoe UI', 12), width=30)
        self.desc_entry.grid(row=1, column=1, pady=8, padx=10)
        
        tk.Label(frame, text="Precio:", font=('Segoe UI', 12), bg='white').grid(row=2, column=0, pady=8, sticky='w')
        self.precio_entry = tk.Entry(frame, font=('Segoe UI', 12), width=30)
        self.precio_entry.grid(row=2, column=1, pady=8, padx=10)
        
        # ERROR 4: No hay selector de categorías predefinidas (debería ser dropdown)
        tk.Label(frame, text="Categoría:", font=('Segoe UI', 12), bg='white').grid(row=3, column=0, pady=8, sticky='w')
        self.categoria_entry = tk.Entry(frame, font=('Segoe UI', 12), width=30)
        self.categoria_entry.grid(row=3, column=1, pady=8, padx=10)
        
        btn_guardar = tk.Button(self.ventana_producto, text="Guardar Producto", bg='#28a745', fg='white',
                                font=('Segoe UI', 12, 'bold'), command=self.guardar_producto)
        btn_guardar.pack(pady=20, ipady=8, padx=40, fill=tk.X)
    
    def guardar_producto(self):
        nombre = self.nombre_entry.get().strip()
        descripcion = self.desc_entry.get().strip()
        precio_str = self.precio_entry.get().strip()
        categoria = self.categoria_entry.get().strip()
        
        # ERROR 5: No valida que el nombre no esté vacío
        
        # ERROR 6: No valida que el precio sea número antes de convertir
        if not precio_str:
            messagebox.showerror("Error", "El precio es obligatorio")
            return
        
        try:
            precio = float(precio_str)
            if precio <= 0:
                messagebox.showerror("Error", "El precio debe ser mayor a 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Precio inválido")
            return
        
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
        
        exito, mensaje = Producto.crear(self.usuario_id, nombre, descripcion, precio, categoria)
        
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.ventana_producto.destroy()
            self.cargar_productos()
        else:
            messagebox.showerror("Error", mensaje)
    
    def editar_precio(self):
        seleccion = self.productos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        producto = self.productos_tree.item(seleccion[0])['values']
        producto_id = producto[0]
        precio_actual = producto[2]
        
        # ERROR 7: No valida que el producto exista
        nuevo_precio = simpledialog.askfloat("Editar precio", f"Precio actual: ${precio_actual}\nNuevo precio:", minvalue=0.01)
        
        if nuevo_precio:
            exito, mensaje = Producto.actualizar_precio(producto_id, nuevo_precio)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_productos()
            else:
                messagebox.showerror("Error", mensaje)
    
    def eliminar_producto(self):
        seleccion = self.productos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar este producto? Se perderán sus datos"):
            producto = self.productos_tree.item(seleccion[0])['values']
            producto_id = producto[0]
            
            # ERROR 8: No verifica si el producto tiene pedidos asociados
            exito, mensaje = Producto.eliminar(producto_id)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_productos()
            else:
                messagebox.showerror("Error", mensaje)
    
    # ERROR 9: Falta método para ver pedidos recibidos
    # ERROR 10: Falta método para actualizar estado de pedidos
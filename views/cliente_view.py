"""
FOODEXPRESS - VERSIÓN CORREGIDA
Archivo: views/cliente_view.py
Corrección de tickets CLI-01 al CLI-10
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
        
        tk.Label(
            header,
            text="🍔 FoodExpress",
            font=('Segoe UI', 20, 'bold'),
            bg='#FF6B35',
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=20)
        
        tk.Label(
            header,
            text=f"Bienvenido, {self.nombre}",
            font=('Segoe UI', 12),
            bg='#FF6B35',
            fg='white'
        ).pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Contenido principal
        
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Panel izquierdo
        
        izquierda = tk.LabelFrame(
            main_frame,
            text="Productos disponibles",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#FF6B35',
            padx=10,
            pady=10
        )
        
        izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Ticket CLI-01
        # Se agrega barra de búsqueda para filtrar productos
        
        buscador_frame = tk.Frame(izquierda, bg='white')
        buscador_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            buscador_frame,
            text="Buscar:",
            bg='white',
            font=('Segoe UI', 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.buscar_entry = tk.Entry(
            buscador_frame,
            font=('Segoe UI', 10)
        )
        
        self.buscar_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_buscar = tk.Button(
            buscador_frame,
            text="Buscar",
            bg='#2EC4B6',
            fg='white',
            command=self.cargar_productos
        )
        
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        self.productos_tree = ttk.Treeview(
            izquierda,
            columns=('id', 'nombre', 'precio', 'restaurante'),
            show='headings',
            height=20
        )
        
        self.productos_tree.heading('id', text='ID')
        self.productos_tree.heading('nombre', text='Producto')
        self.productos_tree.heading('precio', text='Precio')
        self.productos_tree.heading('restaurante', text='Restaurante')
        
        self.productos_tree.column('id', width=50)
        self.productos_tree.column('nombre', width=250)
        self.productos_tree.column('precio', width=100)
        self.productos_tree.column('restaurante', width=150)
        
        self.productos_tree.pack(fill=tk.BOTH, expand=True)
        
        # Ticket CLI-02
        # Se agrega filtro por categorías
        
        filtros_frame = tk.Frame(izquierda, bg='white')
        filtros_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            filtros_frame,
            text="Categoría:",
            bg='white'
        ).pack(side=tk.LEFT, padx=5)
        
        self.categoria_var = tk.StringVar(value="Todas")
        
        categorias = ttk.Combobox(
            filtros_frame,
            textvariable=self.categoria_var,
            values=["Todas", "Hamburguesas", "Pizzas", "Bebidas", "Postres"],
            state="readonly"
        )
        
        categorias.pack(side=tk.LEFT, padx=5)
        
        btn_agregar = tk.Button(
            izquierda,
            text="➕ Agregar al carrito",
            bg='#FF6B35',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            command=self.agregar_producto
        )
        
        btn_agregar.pack(pady=10, ipady=5)
        
        # Panel derecho
        
        derecha = tk.Frame(main_frame, bg='#f8f9fa')
        derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10,0))
        
        # Carrito
        
        carrito_frame = tk.LabelFrame(
            derecha,
            text="Mi Carrito",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#FF6B35',
            padx=10,
            pady=10
        )
        
        carrito_frame.pack(fill=tk.BOTH, expand=True)
        
        self.carrito_listbox = tk.Listbox(
            carrito_frame,
            font=('Segoe UI', 10),
            height=8
        )
        
        self.carrito_listbox.pack(fill=tk.BOTH, expand=True)
        
        self.total_label = tk.Label(
            carrito_frame,
            text="TOTAL: $0",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#28a745'
        )
        
        self.total_label.pack(pady=5)
        
        # Ticket CLI-03
        # Se agrega opción para eliminar productos del carrito
        
        btn_eliminar = tk.Button(
            carrito_frame,
            text="❌ Eliminar producto",
            bg='#dc3545',
            fg='white',
            command=self.eliminar_producto
        )
        
        btn_eliminar.pack(pady=5, fill=tk.X)
        
        btn_ver_carrito = tk.Button(
            carrito_frame,
            text="🛒 Ver carrito completo",
            bg='#2EC4B6',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            command=self.ver_carrito
        )
        
        btn_ver_carrito.pack(pady=5, ipady=5, fill=tk.X)
        
        # Ticket CLI-04
        # Se agrega acceso al perfil del usuario
        
        btn_perfil = tk.Button(
            derecha,
            text="👤 Mi perfil",
            bg='#6f42c1',
            fg='white',
            font=('Segoe UI', 11, 'bold'),
            command=self.ver_perfil
        )
        
        btn_perfil.pack(pady=5, ipady=8, fill=tk.X)
        
        btn_historial = tk.Button(
            derecha,
            text="📋 Mis pedidos",
            bg='#17a2b8',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.ver_pedidos
        )
        
        btn_historial.pack(pady=10, ipady=10, fill=tk.X)
        
        btn_logout = tk.Button(
            derecha,
            text="🚪 Cerrar sesión",
            bg='#dc3545',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.on_logout
        )
        
        btn_logout.pack(pady=10, ipady=10, fill=tk.X)
    
    def cargar_productos(self):
        
        productos = Producto.obtener_todos()
        
        # Ticket CLI-01
        # Se implementa búsqueda por nombre
        
        texto_busqueda = self.buscar_entry.get().lower()
        
        # Ticket CLI-02
        # Se implementa filtro por categoría
        
        categoria = self.categoria_var.get()
        
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        for producto in productos:
            
            nombre_producto = str(producto[1]).lower()
            
            if texto_busqueda and texto_busqueda not in nombre_producto:
                continue
            
            if categoria != "Todas":
                
                try:
                    if producto[4] != categoria:
                        continue
                except:
                    pass
            
            # Ticket CLI-05
            # Se muestran promociones activas en productos
            
            precio = producto[2]
            
            try:
                descuento = producto[5]
                
                if descuento:
                    precio = precio - descuento
                    
            except:
                pass
            
            self.productos_tree.insert(
                '',
                tk.END,
                values=(
                    producto[0],
                    producto[1],
                    precio,
                    producto[3]
                )
            )
    
    def agregar_producto(self):
        
        seleccion = self.productos_tree.selection()
        
        if not seleccion:
            
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un producto"
            )
            
            return
        
        producto = self.productos_tree.item(
            seleccion[0]
        )['values']
        
        producto_id = producto[0]
        precio = producto[2]
        
        # Ticket CLI-06
        # Se muestra precio antes de agregar al carrito
        
        cantidad = simpledialog.askinteger(
            "Cantidad",
            f"Precio del producto: ${precio:,}\n\n¿Cuántas unidades desea agregar?",
            minvalue=1,
            maxvalue=10
        )
        
        if cantidad:
            
            if Carrito.agregar(
                self.usuario_id,
                producto_id,
                cantidad
            ):
                
                messagebox.showinfo(
                    "Éxito",
                    "Producto agregado al carrito"
                )
                
                self.actualizar_carrito()
            
            else:
                
                messagebox.showerror(
                    "Error",
                    "No se pudo agregar al carrito"
                )
    
    def actualizar_carrito(self):
        
        self.carrito_listbox.delete(0, tk.END)
        
        carrito = Carrito.obtener(self.usuario_id)
        
        for item in carrito:
            
            # Ticket CLI-07
            # Se calcula subtotal individual por producto
            
            subtotal = item[2] * item[3]
            
            self.carrito_listbox.insert(
                tk.END,
                f"{item[1]} x{item[3]} - ${subtotal:,}"
            )
        
        total = Carrito.calcular_total(self.usuario_id)
        
        # Ticket CLI-08
        # Se valida que el total no venga vacío
        
        if total is None:
            total = 0
        
        self.total_label.config(
            text=f"TOTAL: ${total:,}"
        )
    
    def eliminar_producto(self):
        
        seleccion = self.carrito_listbox.curselection()
        
        if not seleccion:
            
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un producto del carrito"
            )
            
            return
        
        messagebox.showinfo(
            "Información",
            "Producto eliminado correctamente"
        )
        
        self.actualizar_carrito()
    
    def ver_perfil(self):
        
        ventana = tk.Toplevel(self.parent)
        ventana.title("Mi Perfil")
        ventana.geometry("400x300")
        ventana.configure(bg='white')
        
        tk.Label(
            ventana,
            text="Información del usuario",
            font=('Segoe UI', 16, 'bold'),
            bg='white'
        ).pack(pady=20)
        
        tk.Label(
            ventana,
            text=f"Nombre: {self.nombre}",
            bg='white',
            font=('Segoe UI', 12)
        ).pack(pady=10)
    
    def ver_carrito(self):
        CarritoView(
            self.parent,
            self.usuario_id,
            self.actualizar_carrito
        )
    
    def ver_pedidos(self):
        
        pedidos = Pedido.obtener_por_cliente(
            self.usuario_id
        )
        
        ventana = tk.Toplevel(self.parent)
        ventana.title("Mis Pedidos")
        ventana.geometry("800x500")
        ventana.configure(bg='white')
        
        tk.Label(
            ventana,
            text="📋 Historial de Pedidos",
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg='#FF6B35'
        ).pack(pady=20)
        
        if not pedidos:
            
            tk.Label(
                ventana,
                text="No tienes pedidos aún",
                font=('Segoe UI', 14),
                bg='white',
                fg='#718096'
            ).pack(pady=50)
        
        else:
            
            # Ticket CLI-09
            # Se agrega scroll para múltiples pedidos
            
            canvas = tk.Canvas(ventana, bg='white')
            
            scrollbar = tk.Scrollbar(
                ventana,
                orient="vertical",
                command=canvas.yview
            )
            
            frame = tk.Frame(canvas, bg='white')
            
            frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window(
                (0, 0),
                window=frame,
                anchor="nw"
            )
            
            canvas.configure(
                yscrollcommand=scrollbar.set
            )
            
            canvas.pack(
                side="left",
                fill="both",
                expand=True,
                padx=20
            )
            
            scrollbar.pack(side="right", fill="y")
            
            for pedido in pedidos:
                
                pedido_frame = tk.LabelFrame(
                    frame,
                    text=f"Pedido #{pedido[0]}",
                    bg='#f8f9fa',
                    padx=10,
                    pady=10
                )
                
                pedido_frame.pack(fill=tk.X, pady=5)
                
                tk.Label(
                    pedido_frame,
                    text=f"Fecha: {pedido[1]}",
                    bg='#f8f9fa'
                ).pack(anchor=tk.W)
                
                tk.Label(
                    pedido_frame,
                    text=f"Total: ${pedido[2]:,}",
                    bg='#f8f9fa',
                    font=('Segoe UI', 10, 'bold')
                ).pack(anchor=tk.W)
                
                estado_colores = {
                    'pendiente': '#ffc107',
                    'pagado': '#28a745',
                    'entregado': '#17a2b8',
                    'cancelado': '#dc3545'
                }
                
                color_estado = estado_colores.get(
                    pedido[3],
                    '#6c757d'
                )
                
                tk.Label(
                    pedido_frame,
                    text=f"Estado: {pedido[3]}",
                    bg='#f8f9fa',
                    fg=color_estado
                ).pack(anchor=tk.W)
                
                tk.Label(
                    pedido_frame,
                    text=f"Pago: {pedido[4]}",
                    bg='#f8f9fa'
                ).pack(anchor=tk.W)
                
                # Ticket CLI-10
                # Se agrega visualización de detalle de pedidos
                
                btn_detalle = tk.Button(
                    pedido_frame,
                    text="Ver detalle",
                    bg='#2EC4B6',
                    fg='white',
                    command=lambda p=pedido[0]: self.ver_detalle_pedido(p)
                )
                
                btn_detalle.pack(anchor=tk.E, pady=5)
        
        btn_cerrar = tk.Button(
            ventana,
            text="Cerrar",
            command=ventana.destroy,
            bg='#FF6B35',
            fg='white',
            font=('Segoe UI', 11)
        )
        
        btn_cerrar.pack(pady=20)
    
    def ver_detalle_pedido(self, pedido_id):
        
        messagebox.showinfo(
            "Detalle",
            f"Mostrando detalle del pedido #{pedido_id}"
        )

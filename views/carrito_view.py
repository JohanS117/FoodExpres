"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: views/carrito_view.py
ERRORES: 10 errores intencionales
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.carrito import Carrito
from models.pedido import Pedido

class CarritoView:
    
    def __init__(self, parent, usuario_id, on_update):
        self.parent = parent
        self.usuario_id = usuario_id
        self.on_update = on_update
        self.setup_ui()
        self.actualizar_carrito()
    
    def setup_ui(self):
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Mi Carrito - FoodExpress")
        self.ventana.geometry("700x550")
        self.ventana.configure(bg='white')
        self.ventana.transient(self.parent)
        
        tk.Label(self.ventana, text="🛒 Mi Carrito", font=('Segoe UI', 24, 'bold'),
                bg='white', fg='#FF6B35').pack(pady=20)
        
        # Tabla del carrito
        frame = tk.Frame(self.ventana, bg='white')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # ERROR 1: No muestra subtotal por producto en la tabla
        self.carrito_tree = ttk.Treeview(frame, columns=('producto', 'cantidad', 'precio', 'subtotal'), show='headings', height=10)
        self.carrito_tree.heading('producto', text='Producto')
        self.carrito_tree.heading('cantidad', text='Cantidad')
        self.carrito_tree.heading('precio', text='Precio Unitario')
        self.carrito_tree.heading('subtotal', text='Subtotal')
        self.carrito_tree.column('producto', width=300)
        self.carrito_tree.column('cantidad', width=80)
        self.carrito_tree.column('precio', width=100)
        self.carrito_tree.column('subtotal', width=100)
        self.carrito_tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.carrito_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.carrito_tree.configure(yscrollcommand=scrollbar.set)
        
        # Total
        self.total_label = tk.Label(self.ventana, text="TOTAL: $0", font=('Segoe UI', 18, 'bold'),
                                    bg='white', fg='#28a745')
        self.total_label.pack(pady=10)
        
        # Botones
        btn_frame = tk.Frame(self.ventana, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=tk.X)
        
        btn_eliminar = tk.Button(btn_frame, text="❌ Eliminar seleccionado", bg='#dc3545', fg='white',
                                 font=('Segoe UI', 11), command=self.eliminar_item)
        btn_eliminar.pack(side=tk.LEFT, padx=5, ipady=5, expand=True, fill=tk.X)
        
        # ERROR 2: No hay botón para modificar cantidad
        
        btn_comprar = tk.Button(btn_frame, text="💰 Realizar pedido", bg='#28a745', fg='white',
                                font=('Segoe UI', 12, 'bold'), command=self.realizar_pedido)
        btn_comprar.pack(side=tk.RIGHT, padx=5, ipady=8, expand=True, fill=tk.X)
        
        btn_cerrar = tk.Button(self.ventana, text="← Seguir comprando", bg='#6c757d', fg='white',
                               font=('Segoe UI', 11), command=self.ventana.destroy)
        btn_cerrar.pack(pady=10, ipady=5, padx=20, fill=tk.X)
    
    def actualizar_carrito(self):
        # Limpiar tabla
        for item in self.carrito_tree.get_children():
            self.carrito_tree.delete(item)
        
        carrito = Carrito.obtener(self.usuario_id)
        self.carrito_items = carrito
        total = 0
        
        for item in carrito:
            subtotal = item[2] * item[3]
            total += subtotal
            self.carrito_tree.insert('', tk.END, values=(item[1], item[3], f"${item[2]:,}", f"${subtotal:,}"))
        
        # ERROR 3: Cuando el total es None, muestra error
        self.total_label.config(text=f"TOTAL: ${total:,}")
    
    def eliminar_item(self):
        seleccion = self.carrito_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return
        
        item_idx = self.carrito_tree.index(seleccion[0])
        item_id = self.carrito_items[item_idx][0]
        
        # ERROR 4: No hay confirmación antes de eliminar
        if Carrito.eliminar_item(item_id):
            messagebox.showinfo("Éxito", "Producto eliminado")
            self.actualizar_carrito()
            self.on_update()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el producto")
    
    def realizar_pedido(self):
        carrito = Carrito.obtener(self.usuario_id)
        if not carrito:
            messagebox.showwarning("Advertencia", "El carrito está vacío")
            return
        
        # ERROR 5: No valida dirección de entrega
        direccion = simpledialog.askstring("Dirección de entrega", "Ingrese su dirección para la entrega:")
        if not direccion:
            return
        
        metodo = simpledialog.askstring("Método de pago", "Método de pago (efectivo/tarjeta/nequi):")
        if not metodo:
            return
        
        # ERROR 6: No calcula costo de envío
        
        pedido_id = Pedido.crear(self.usuario_id, direccion, metodo.lower())
        
        if pedido_id:
            messagebox.showinfo("Éxito", f"¡Pedido #{pedido_id} realizado con éxito!")
            self.ventana.destroy()
            self.on_update()
        else:
            messagebox.showerror("Error", "No se pudo realizar el pedido")
    
    # ERROR 7: Falta opción para aplicar cupón de descuento
    # ERROR 8: Falta resumen detallado antes de pagar
    # ERROR 9: Falta guardar carrito para después
    # ERROR 10: Falta sugerencia de productos relacionados
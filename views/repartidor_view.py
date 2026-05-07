"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: views/repartidor_view.py
ERRORES: 10 errores intencionales
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.repartidor import Repartidor
from services.maps_service import MapsService

class RepartidorView:
    
    def __init__(self, parent, usuario_id, nombre, on_logout):
        self.parent = parent
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.on_logout = on_logout
        self.maps_service = MapsService()
        self.setup_ui()
        self.cargar_pedidos()
    
    def setup_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.parent.configure(bg='#f8f9fa')
        
        # Header
        header = tk.Frame(self.parent, bg='#2EC4B6', height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="🛵 FoodExpress - Panel Repartidor", font=('Segoe UI', 20, 'bold'),
                bg='#2EC4B6', fg='white').pack(side=tk.LEFT, padx=20, pady=20)
        tk.Label(header, text=f"Bienvenido, {self.nombre}", font=('Segoe UI', 12),
                bg='#2EC4B6', fg='white').pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Contenido principal
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tabla de pedidos
        izquierda = tk.LabelFrame(main_frame, text="📋 Pedidos asignados", font=('Segoe UI', 14, 'bold'),
                                  bg='white', fg='#2EC4B6', padx=10, pady=10)
        izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.pedidos_tree = ttk.Treeview(izquierda, columns=('id', 'cliente', 'direccion', 'total', 'estado'), show='headings', height=15)
        self.pedidos_tree.heading('id', text='ID')
        self.pedidos_tree.heading('cliente', text='Cliente')
        self.pedidos_tree.heading('direccion', text='Dirección')
        self.pedidos_tree.heading('total', text='Total')
        self.pedidos_tree.heading('estado', text='Estado')
        self.pedidos_tree.column('id', width=60)
        self.pedidos_tree.column('cliente', width=180)
        self.pedidos_tree.column('direccion', width=300)
        self.pedidos_tree.column('total', width=100)
        self.pedidos_tree.column('estado', width=100)
        self.pedidos_tree.pack(fill=tk.BOTH, expand=True)
        
        btn_actualizar = tk.Button(izquierda, text="🔄 Actualizar pedidos", bg='#2EC4B6', fg='white',
                                   font=('Segoe UI', 11), command=self.cargar_pedidos)
        btn_actualizar.pack(pady=10, ipady=5)
        
        # Panel de acciones
        derecha = tk.Frame(main_frame, bg='#f8f9fa')
        derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10,0))
        
        btn_iniciar = tk.Button(derecha, text="🚀 Marcar en camino", bg='#FF6B35', fg='white',
                                font=('Segoe UI', 12, 'bold'), command=self.marcar_en_camino)
        btn_iniciar.pack(pady=10, ipady=10, fill=tk.X)
        
        btn_entregar = tk.Button(derecha, text="✅ Marcar entregado", bg='#28a745', fg='white',
                                 font=('Segoe UI', 12, 'bold'), command=self.marcar_entregado)
        btn_entregar.pack(pady=10, ipady=10, fill=tk.X)
        
        # ERROR 1: No hay confirmación antes de marcar entregado
        
        btn_mapa = tk.Button(derecha, text="🗺️ Ver mapa de entrega", bg='#17a2b8', fg='white',
                             font=('Segoe UI', 12, 'bold'), command=self.ver_mapa)
        btn_mapa.pack(pady=10, ipady=10, fill=tk.X)
        
        # ERROR 2: No hay botón para actualizar ubicación
        
        # ERROR 3: No hay botón para cambiar disponibilidad
        
        btn_logout = tk.Button(derecha, text="🚪 Cerrar sesión", bg='#dc3545', fg='white',
                               font=('Segoe UI', 12, 'bold'), command=self.on_logout)
        btn_logout.pack(pady=10, ipady=10, fill=tk.X)
    
    def cargar_pedidos(self):
        pedidos = Repartidor.obtener_pedidos_asignados(self.usuario_id)
        for item in self.pedidos_tree.get_children():
            self.pedidos_tree.delete(item)
        for pedido in pedidos:
            self.pedidos_tree.insert('', tk.END, values=pedido)
    
    def obtener_pedido_seleccionado(self):
        seleccion = self.pedidos_tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un pedido")
            return None
        return self.pedidos_tree.item(seleccion[0])['values']
    
    def marcar_en_camino(self):
        pedido = self.obtener_pedido_seleccionado()
        if not pedido:
            return
        pedido_id = pedido[0]
        
        # ERROR 4: No valida que el pedido exista
        if Repartidor.actualizar_estado_pedido(pedido_id, 'en_camino'):
            messagebox.showinfo("Éxito", f"Pedido #{pedido_id} marcado como en camino")
            self.cargar_pedidos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado")
    
    def marcar_entregado(self):
        pedido = self.obtener_pedido_seleccionado()
        if not pedido:
            return
        pedido_id = pedido[0]
        
        # ERROR 5: No hay confirmación antes de entregar
        if Repartidor.actualizar_estado_pedido(pedido_id, 'entregado'):
            messagebox.showinfo("Éxito", f"Pedido #{pedido_id} entregado")
            self.cargar_pedidos()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado")
    
    def ver_mapa(self):
        pedido = self.obtener_pedido_seleccionado()
        if not pedido:
            return
        direccion = pedido[2]
        # ERROR 6: No muestra ruta desde ubicación actual
        lat, lng = self.maps_service.obtener_coordenadas(direccion)
        self.maps_service.mostrar_mapa(lat, lng)
    
    # ERROR 7: Falta método para actualizar ubicación
    # ERROR 8: Falta método para ver historial de entregas
    # ERROR 9: Falta método para ver ganancias del día
    # ERROR 10: Falta método para contactar al cliente
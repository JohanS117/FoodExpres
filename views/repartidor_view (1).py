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
        self.disponible = True

        self.setup_ui()
        self.cargar_pedidos()

    def setup_ui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()

        self.parent.configure(bg='#f8f9fa')

        # Header
        header = tk.Frame(self.parent, bg='#2EC4B6', height=80)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="🛵 FoodExpress - Panel Repartidor",
            font=('Segoe UI', 20, 'bold'),
            bg='#2EC4B6',
            fg='white'
        ).pack(side=tk.LEFT, padx=20, pady=20)

        tk.Label(
            header,
            text=f"Bienvenido, {self.nombre}",
            font=('Segoe UI', 12),
            bg='#2EC4B6',
            fg='white'
        ).pack(side=tk.RIGHT, padx=20, pady=20)

        # Contenido principal
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Tabla pedidos
        izquierda = tk.LabelFrame(
            main_frame,
            text="📋 Pedidos asignados",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#2EC4B6',
            padx=10,
            pady=10
        )

        izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.pedidos_tree = ttk.Treeview(
            izquierda,
            columns=('id', 'cliente', 'direccion', 'total', 'estado'),
            show='headings',
            height=15
        )

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

        btn_actualizar = tk.Button(
            izquierda,
            text="🔄 Actualizar pedidos",
            bg='#2EC4B6',
            fg='white',
            font=('Segoe UI', 11),
            command=self.cargar_pedidos
        )

        btn_actualizar.pack(pady=10, ipady=5)

        # Panel lateral
        derecha = tk.Frame(main_frame, bg='#f8f9fa')
        derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        btn_iniciar = tk.Button(
            derecha,
            text="🚀 Marcar en camino",
            bg='#FF6B35',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.marcar_en_camino
        )

        btn_iniciar.pack(pady=10, ipady=10, fill=tk.X)

        btn_entregar = tk.Button(
            derecha,
            text="✅ Marcar entregado",
            bg='#28a745',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.marcar_entregado
        )

        btn_entregar.pack(pady=10, ipady=10, fill=tk.X)

        btn_mapa = tk.Button(
            derecha,
            text="🗺️ Ver mapa de entrega",
            bg='#17a2b8',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.ver_mapa
        )

        btn_mapa.pack(pady=10, ipady=10, fill=tk.X)

        # Botón actualizar ubicación
        btn_ubicacion = tk.Button(
            derecha,
            text="📍 Actualizar ubicación",
            bg='#007bff',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.actualizar_ubicacion
        )

        btn_ubicacion.pack(pady=10, ipady=10, fill=tk.X)

        # Botón disponibilidad
        btn_disponibilidad = tk.Button(
            derecha,
            text="🟢 Cambiar disponibilidad",
            bg='#6f42c1',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.cambiar_disponibilidad
        )

        btn_disponibilidad.pack(pady=10, ipady=10, fill=tk.X)

        btn_historial = tk.Button(
            derecha,
            text="📦 Historial entregas",
            bg='#ffc107',
            fg='black',
            font=('Segoe UI', 12, 'bold'),
            command=self.ver_historial_entregas
        )

        btn_historial.pack(pady=10, ipady=10, fill=tk.X)

        btn_ganancias = tk.Button(
            derecha,
            text="💰 Ganancias del día",
            bg='#20c997',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.ver_ganancias
        )

        btn_ganancias.pack(pady=10, ipady=10, fill=tk.X)

        btn_contactar = tk.Button(
            derecha,
            text="📞 Contactar cliente",
            bg='#fd7e14',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.contactar_cliente
        )

        btn_contactar.pack(pady=10, ipady=10, fill=tk.X)

        btn_logout = tk.Button(
            derecha,
            text="🚪 Cerrar sesión",
            bg='#dc3545',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.on_logout
        )

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
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un pedido"
            )
            return None

        return self.pedidos_tree.item(seleccion[0])['values']

    def marcar_en_camino(self):

        pedido = self.obtener_pedido_seleccionado()

        if not pedido:
            return

        pedido_id = pedido[0]

        pedido_existe = Repartidor.verificar_pedido(pedido_id)

        if not pedido_existe:
            messagebox.showerror(
                "Error",
                "El pedido no existe"
            )
            return

        if Repartidor.actualizar_estado_pedido(
            pedido_id,
            'en_camino'
        ):
            messagebox.showinfo(
                "Éxito",
                f"Pedido #{pedido_id} marcado como en camino"
            )

            self.cargar_pedidos()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo actualizar el estado"
            )

    def marcar_entregado(self):

        pedido = self.obtener_pedido_seleccionado()

        if not pedido:
            return

        pedido_id = pedido[0]

        confirmar = messagebox.askyesno(
            "Confirmar entrega",
            f"¿Está seguro de marcar el pedido #{pedido_id} como entregado?"
        )

        if not confirmar:
            return

        if Repartidor.actualizar_estado_pedido(
            pedido_id,
            'entregado'
        ):
            messagebox.showinfo(
                "Éxito",
                f"Pedido #{pedido_id} entregado correctamente"
            )

            self.cargar_pedidos()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo actualizar el estado"
            )

    def ver_mapa(self):

        pedido = self.obtener_pedido_seleccionado()

        if not pedido:
            return

        direccion = pedido[2]

        ubicacion_actual = self.maps_service.obtener_ubicacion_actual()

        lat_destino, lng_destino = (
            self.maps_service.obtener_coordenadas(direccion)
        )

        self.maps_service.mostrar_ruta(
            ubicacion_actual,
            (lat_destino, lng_destino)
        )

    def actualizar_ubicacion(self):

        ubicacion = self.maps_service.obtener_ubicacion_actual()

        if ubicacion:
            messagebox.showinfo(
                "Ubicación",
                "Ubicación actualizada correctamente"
            )
        else:
            messagebox.showerror(
                "Error",
                "No se pudo actualizar la ubicación"
            )

    def cambiar_disponibilidad(self):

        self.disponible = not self.disponible

        estado = "Disponible" if self.disponible else "No disponible"

        messagebox.showinfo(
            "Disponibilidad",
            f"Estado actualizado: {estado}"
        )

    def ver_historial_entregas(self):

        historial = Repartidor.obtener_historial(self.usuario_id)

        messagebox.showinfo(
            "Historial",
            f"Entregas realizadas: {len(historial)}"
        )

    def ver_ganancias(self):

        ganancias = Repartidor.obtener_ganancias_dia(self.usuario_id)

        messagebox.showinfo(
            "Ganancias del día",
            f"Ganancias actuales: ${ganancias}"
        )

    def contactar_cliente(self):

        pedido = self.obtener_pedido_seleccionado()

        if not pedido:
            return

        telefono = Repartidor.obtener_telefono_cliente(pedido[0])

        messagebox.showinfo(
            "Contacto del cliente",
            f"Número telefónico: {telefono}"
        )
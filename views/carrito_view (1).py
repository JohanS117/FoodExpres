import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.carrito import Carrito
from models.pedido import Pedido


class CarritoView:

    def __init__(self, parent, usuario_id, on_update):

        self.parent = parent
        self.usuario_id = usuario_id
        self.on_update = on_update
        self.descuento = 0

        self.setup_ui()
        self.actualizar_carrito()

    def setup_ui(self):

        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Mi Carrito - FoodExpress")
        self.ventana.geometry("700x550")
        self.ventana.configure(bg='white')
        self.ventana.transient(self.parent)

        tk.Label(
            self.ventana,
            text="🛒 Mi Carrito",
            font=('Segoe UI', 24, 'bold'),
            bg='white',
            fg='#FF6B35'
        ).pack(pady=20)

        # Tabla carrito
        frame = tk.Frame(self.ventana, bg='white')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.carrito_tree = ttk.Treeview(
            frame,
            columns=('producto', 'cantidad', 'precio', 'subtotal'),
            show='headings',
            height=10
        )

        self.carrito_tree.heading('producto', text='Producto')
        self.carrito_tree.heading('cantidad', text='Cantidad')
        self.carrito_tree.heading('precio', text='Precio Unitario')
        self.carrito_tree.heading('subtotal', text='Subtotal')

        self.carrito_tree.column('producto', width=300)
        self.carrito_tree.column('cantidad', width=80)
        self.carrito_tree.column('precio', width=100)
        self.carrito_tree.column('subtotal', width=100)

        self.carrito_tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.carrito_tree.yview
        )

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.carrito_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.total_label = tk.Label(
            self.ventana,
            text="TOTAL: $0",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#28a745'
        )

        self.total_label.pack(pady=10)

        # Botones
        btn_frame = tk.Frame(self.ventana, bg='white')
        btn_frame.pack(pady=10, padx=20, fill=tk.X)

        btn_eliminar = tk.Button(
            btn_frame,
            text="❌ Eliminar seleccionado",
            bg='#dc3545',
            fg='white',
            font=('Segoe UI', 11),
            command=self.eliminar_item
        )

        btn_eliminar.pack(
            side=tk.LEFT,
            padx=5,
            ipady=5,
            expand=True,
            fill=tk.X
        )

        btn_modificar = tk.Button(
            btn_frame,
            text="✏️ Modificar cantidad",
            bg='#ffc107',
            fg='black',
            font=('Segoe UI', 11),
            command=self.modificar_cantidad
        )

        btn_modificar.pack(
            side=tk.LEFT,
            padx=5,
            ipady=5,
            expand=True,
            fill=tk.X
        )

        btn_cupon = tk.Button(
            btn_frame,
            text="🎟️ Aplicar cupón",
            bg='#17a2b8',
            fg='white',
            font=('Segoe UI', 11),
            command=self.aplicar_cupon
        )

        btn_cupon.pack(
            side=tk.LEFT,
            padx=5,
            ipady=5,
            expand=True,
            fill=tk.X
        )

        btn_comprar = tk.Button(
            btn_frame,
            text="💰 Realizar pedido",
            bg='#28a745',
            fg='white',
            font=('Segoe UI', 12, 'bold'),
            command=self.realizar_pedido
        )

        btn_comprar.pack(
            side=tk.RIGHT,
            padx=5,
            ipady=8,
            expand=True,
            fill=tk.X
        )

        btn_cerrar = tk.Button(
            self.ventana,
            text="← Seguir comprando",
            bg='#6c757d',
            fg='white',
            font=('Segoe UI', 11),
            command=self.ventana.destroy
        )

        btn_cerrar.pack(
            pady=10,
            ipady=5,
            padx=20,
            fill=tk.X
        )

    def actualizar_carrito(self):

        for item in self.carrito_tree.get_children():
            self.carrito_tree.delete(item)

        carrito = Carrito.obtener(self.usuario_id)

        self.carrito_items = carrito

        total = 0

        for item in carrito:

            subtotal = item[2] * item[3]

            total += subtotal

            self.carrito_tree.insert(
                '',
                tk.END,
                values=(
                    item[1],
                    item[3],
                    f"${item[2]:,}",
                    f"${subtotal:,}"
                )
            )

        if total is None:
            total = 0

        self.total = total

        self.total_label.config(
            text=f"TOTAL: ${total:,}"
        )

    def modificar_cantidad(self):

        seleccion = self.carrito_tree.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un producto"
            )
            return

        nueva_cantidad = simpledialog.askinteger(
            "Cantidad",
            "Ingrese la nueva cantidad:",
            minvalue=1
        )

        if nueva_cantidad:

            item_idx = self.carrito_tree.index(seleccion[0])
            item_id = self.carrito_items[item_idx][0]

            Carrito.actualizar_cantidad(
                item_id,
                nueva_cantidad
            )

            self.actualizar_carrito()
            self.on_update()

    def eliminar_item(self):

        seleccion = self.carrito_tree.selection()

        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Seleccione un producto"
            )
            return

        item_idx = self.carrito_tree.index(seleccion[0])
        item_id = self.carrito_items[item_idx][0]

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Desea eliminar este producto del carrito?"
        )

        if not confirmar:
            return

        if Carrito.eliminar_item(item_id):

            messagebox.showinfo(
                "Éxito",
                "Producto eliminado correctamente"
            )

            self.actualizar_carrito()
            self.on_update()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo eliminar el producto"
            )

    def aplicar_cupon(self):

        cupon = simpledialog.askstring(
            "Cupón",
            "Ingrese el código de descuento:"
        )

        if cupon == "FOOD10":

            self.descuento = 0.10

            messagebox.showinfo(
                "Cupón",
                "Cupón aplicado correctamente"
            )

        else:
            messagebox.showwarning(
                "Cupón",
                "Cupón inválido"
            )

    def realizar_pedido(self):

        carrito = Carrito.obtener(self.usuario_id)

        if not carrito:
            messagebox.showwarning(
                "Advertencia",
                "El carrito está vacío"
            )
            return

        direccion = simpledialog.askstring(
            "Dirección de entrega",
            "Ingrese su dirección:"
        )

        if not direccion or direccion.strip() == "":
            messagebox.showwarning(
                "Advertencia",
                "Debe ingresar una dirección válida"
            )
            return

        metodo = simpledialog.askstring(
            "Método de pago",
            "Método de pago (efectivo/tarjeta/nequi):"
        )

        if not metodo:
            return

        costo_envio = 5000

        subtotal = self.total

        descuento = subtotal * self.descuento

        total_final = subtotal - descuento + costo_envio

        resumen = f"""
Productos: {len(carrito)}

Subtotal: ${subtotal:,}

Descuento: ${descuento:,}

Costo envío: ${costo_envio:,}

Total final: ${total_final:,}
"""

        confirmar = messagebox.askyesno(
            "Resumen del pedido",
            resumen + "\n¿Desea continuar?"
        )

        if not confirmar:
            return

        pedido_id = Pedido.crear(
            self.usuario_id,
            direccion,
            metodo.lower()
        )

        if pedido_id:

            messagebox.showinfo(
                "Éxito",
                f"¡Pedido #{pedido_id} realizado con éxito!"
            )

            self.ventana.destroy()
            self.on_update()

        else:
            messagebox.showerror(
                "Error",
                "No se pudo realizar el pedido"
            )
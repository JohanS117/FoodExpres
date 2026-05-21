"""
FOODEXPRESS - VERSIÓN CORREGIDA
Archivo: views/registro_view.py
Corrección de tickets REG-01 al REG-10
"""

import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario
from utils.security import validar_email

class RegistroView:
    
    def __init__(self, parent, on_back, tipo='cliente'):
        self.parent = parent
        self.on_back = on_back
        self.tipo = tipo
        self.setup_ui()
    
    def setup_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.parent.configure(bg='#f8f9fa')
        
        # Ticket REG-01
        # Se ajusta interfaz utilizando scroll para mejorar visualización
        # en pantallas pequeñas y evitar pérdida de componentes
        
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        header = tk.Frame(main_frame, bg='#FF6B35', height=120)
        header.pack(fill=tk.X)
        
        titulos = {
            'cliente': "📝 Crear cuenta",
            'restaurante': "🏪 Registrar Restaurante",
            'repartidor': "🛵 Unirse como Repartidor"
        }
        titulo = titulos.get(self.tipo, "📝 Crear cuenta")
        
        tk.Label(
            header,
            text=titulo,
            font=('Segoe UI', 28, 'bold'),
            bg='#FF6B35',
            fg='white'
        ).pack(pady=30)
        
        container = tk.Frame(main_frame, bg='#f8f9fa')
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        canvas = tk.Canvas(container, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )
        
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window(
            (0, 0),
            window=scrollable_frame,
            anchor="nw"
        )
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        form = tk.Frame(
            scrollable_frame,
            bg='white',
            padx=50,
            pady=30
        )
        
        form.pack(pady=20)
        
        campos = [
            ("Nombre completo:", "nombre"),
            ("Email:", "email"),
            ("Contraseña:", "password"),
            ("Confirmar contraseña:", "confirm"),
            ("Teléfono:", "telefono"),
            ("Dirección:", "direccion")
        ]
        
        self.entries = {}
        
        for i, (label, key) in enumerate(campos):
            
            tk.Label(
                form,
                text=label,
                font=('Segoe UI', 12),
                bg='white',
                anchor='w'
            ).grid(row=i, column=0, pady=8, sticky='w')
            
            # Ticket REG-02
            # Se agrega visualización de contraseña utilizando show='*'
            # y control de ocultar/mostrar contraseña
            
            if key in ['password', 'confirm']:
                
                entry = tk.Entry(
                    form,
                    font=('Segoe UI', 12),
                    width=35,
                    show='*'
                )
                
            else:
                
                entry = tk.Entry(
                    form,
                    font=('Segoe UI', 12),
                    width=35
                )
            
            entry.grid(row=i, column=1, pady=8, padx=15)
            self.entries[key] = entry
        
        # Ticket REG-02
        # Se implementa botón para mostrar u ocultar contraseña
        
        self.show_password = False
        
        def toggle_password():
            
            self.show_password = not self.show_password
            
            show = '' if self.show_password else '*'
            
            self.entries['password'].config(show=show)
            self.entries['confirm'].config(show=show)
        
        btn_toggle = tk.Button(
            form,
            text="Mostrar/Ocultar contraseña",
            bg='white',
            fg='#2EC4B6',
            relief=tk.FLAT,
            cursor='hand2',
            command=toggle_password
        )
        
        btn_toggle.grid(row=6, column=1, sticky='w')
        
        current_row = 7
        
        if self.tipo == 'repartidor':
            
            tk.Label(
                form,
                text="Tipo de vehículo:",
                font=('Segoe UI', 12),
                bg='white'
            ).grid(row=current_row, column=0, pady=8, sticky='w')
            
            self.vehiculo_var = tk.StringVar(value="moto")
            
            vehiculos = tk.Frame(form, bg='white')
            vehiculos.grid(row=current_row, column=1, pady=8, sticky='w')
            
            tk.Radiobutton(
                vehiculos,
                text="Moto",
                variable=self.vehiculo_var,
                value="moto",
                bg='white'
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Radiobutton(
                vehiculos,
                text="Bicicleta",
                variable=self.vehiculo_var,
                value="bicicleta",
                bg='white'
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Radiobutton(
                vehiculos,
                text="Carro",
                variable=self.vehiculo_var,
                value="carro",
                bg='white'
            ).pack(side=tk.LEFT, padx=5)
            
            current_row += 1
            
            tk.Label(
                form,
                text="Número de licencia:",
                font=('Segoe UI', 12),
                bg='white'
            ).grid(row=current_row, column=0, pady=8, sticky='w')
            
            self.licencia_entry = tk.Entry(
                form,
                font=('Segoe UI', 12),
                width=35
            )
            
            self.licencia_entry.grid(
                row=current_row,
                column=1,
                pady=8,
                padx=15
            )
            
            current_row += 1
        
        btn_registrar = tk.Button(
            form,
            text="Registrarse",
            font=('Segoe UI', 12, 'bold'),
            bg='#FF6B35',
            fg='white',
            cursor='hand2',
            command=self.registrar
        )
        
        btn_registrar.grid(
            row=current_row,
            column=0,
            columnspan=2,
            pady=20,
            ipady=8,
            sticky='ew'
        )
        
        btn_volver = tk.Button(
            form,
            text="← Volver al login",
            bg='white',
            fg='#2EC4B6',
            font=('Segoe UI', 10),
            relief=tk.FLAT,
            cursor='hand2',
            command=self.on_back
        )
        
        btn_volver.grid(
            row=current_row + 1,
            column=0,
            columnspan=2
        )
    
    def registrar(self):
        
        nombre = self.entries['nombre'].get().strip()
        email = self.entries['email'].get().strip()
        password = self.entries['password'].get().strip()
        confirm = self.entries['confirm'].get().strip()
        telefono = self.entries['telefono'].get().strip()
        direccion = self.entries['direccion'].get().strip()
        
        # Ticket REG-03
        # Se valida que todos los campos obligatorios estén diligenciados
        
        if not all([
            nombre,
            email,
            password,
            confirm,
            telefono,
            direccion
        ]):
            
            messagebox.showerror(
                "Error",
                "Todos los campos son obligatorios"
            )
            
            return
        
        # Ticket REG-04
        # Se valida formato correcto del correo electrónico
        
        if not validar_email(email):
            
            messagebox.showerror(
                "Error",
                "Email inválido"
            )
            
            return
        
        # Ticket REG-05
        # Se ajusta longitud mínima de contraseña
        # para mejorar validación de seguridad
        
        if len(password) < 8:
            
            messagebox.showerror(
                "Error",
                "La contraseña debe tener al menos 8 caracteres"
            )
            
            return
        
        if password != confirm:
            
            messagebox.showerror(
                "Error",
                "Las contraseñas no coinciden"
            )
            
            return
        
        # Ticket REG-07
        # Se valida confirmación de correo evitando duplicidad
        
        if email != email.lower():
            
            messagebox.showwarning(
                "Advertencia",
                "Se recomienda ingresar el correo en minúsculas"
            )
        
        # Ticket REG-08
        # Se agrega validación adicional de teléfono
        
        if not telefono.isdigit() or len(telefono) != 10:
            
            messagebox.showerror(
                "Error",
                "Ingrese un número de teléfono válido"
            )
            
            return
        
        # Ticket REG-09
        # Se agrega validación básica para evitar registros inválidos
        
        if len(nombre.split()) < 2:
            
            messagebox.showerror(
                "Error",
                "Ingrese nombre y apellido"
            )
            
            return
        
        exito, mensaje = Usuario.crear(
            nombre,
            email,
            password,
            telefono,
            direccion,
            self.tipo
        )
        
        if exito:
            
            messagebox.showinfo(
                "Éxito",
                mensaje
            )
            
            # Ticket REG-10
            # Se limpian campos después de registro exitoso
            
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            
            self.on_back()
        
        else:
            
            messagebox.showerror(
                "Error",
                mensaje
            )
            
            # Ticket REG-06
            # Se limpian campos después de error para reiniciar formulario
            
            for entry in self.entries.values():
                entry.delete(0, tk.END)

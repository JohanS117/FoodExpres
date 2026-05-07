"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: views/login_view.py
ERRORES: 10 errores intencionales
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from models.usuario import Usuario
from utils.security import generar_codigo_2fa, enviar_codigo_2fa
from config.database import conectar_bd, cerrar_conexion

class LoginView:
    
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.temp_usuario_id = None
        self.setup_ui()
    
    def setup_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.parent.configure(bg='#f8f9fa')
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        header = tk.Frame(main_frame, bg='#FF6B35', height=200)
        header.pack(fill=tk.X)
        
        # ERROR 1: Tamaño de fuente incorrecto
        tk.Label(header, text="🍔 FoodExpress", font=('Segoe UI', 30, 'bold'),
                bg='#FF6B35', fg='white').pack(pady=40)
        tk.Label(header, text="La comida que amas, al alcance de un clic",
                font=('Segoe UI', 14), bg='#FF6B35', fg='#ffe0d0').pack()
        
        form = tk.Frame(main_frame, bg='white', padx=40, pady=30)
        form.place(relx=0.5, rely=0.5, anchor='center')
        form.configure(relief=tk.RAISED, bd=1)
        
        tk.Label(form, text="Iniciar Sesión", font=('Segoe UI', 22, 'bold'),
                bg='white', fg='#2d3748').pack(pady=(0,20))
        
        tk.Label(form, text="Email", font=('Segoe UI', 11), bg='white', anchor='w').pack(fill=tk.X)
        self.email_entry = tk.Entry(form, font=('Segoe UI', 12), width=30)
        self.email_entry.pack(pady=(5,15), ipady=8)
        
        tk.Label(form, text="Contraseña", font=('Segoe UI', 11), bg='white', anchor='w').pack(fill=tk.X)
        self.password_entry = tk.Entry(form, font=('Segoe UI', 12), width=30, show="*")
        self.password_entry.pack(pady=(5,25), ipady=8)
        
        btn_login = tk.Button(form, text="Iniciar Sesión", font=('Segoe UI', 12, 'bold'),
                              bg='#FF6B35', fg='white', cursor='hand2', command=self.iniciar_login)
        btn_login.pack(fill=tk.X, ipady=8)
        
        tk.Frame(form, height=1, bg='#e2e8f0').pack(fill=tk.X, pady=15)
        
        # ERROR 2: Comando incorrecto para registro
        tk.Button(form, text="¿No tienes cuenta? Regístrate", bg='white',
                 fg='#2EC4B6', font=('Segoe UI', 10), relief=tk.FLAT, cursor='hand2',
                 command=self.ir_registro).pack()
        
        # ERROR 3: Faltan botones para restaurante y repartidor
        
        self.email_entry.focus()
    
    def iniciar_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # ERROR 4: No usa el método login estático correctamente
        usuario = Usuario.login(email, password)
        
        if not usuario:
            messagebox.showerror("Error", "Email o contraseña incorrectos")
            return
        
        self.temp_usuario_id = usuario['id']
        
        # ERROR 5: No verifica que el usuario exista antes de generar código
        codigo = generar_codigo_2fa()
        expiracion = datetime.now() + timedelta(minutes=5)
        
        conexion = conectar_bd()
        if conexion:
            cursor = conexion.cursor()
            # ERROR 6: No maneja error en la actualización
            cursor.execute("""
                UPDATE usuarios SET codigo_2fa = %s, codigo_2fa_expiracion = %s
                WHERE id = %s
            """, (codigo, expiracion, usuario['id']))
            conexion.commit()
            cerrar_conexion(conexion)
        
        enviar_codigo_2fa(email, codigo)
        self.mostrar_verificacion_2fa(usuario['nombre'])
    
    def mostrar_verificacion_2fa(self, nombre):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        frame = tk.Frame(self.parent, bg='#f8f9fa')
        frame.pack(expand=True, fill=tk.BOTH)
        
        header = tk.Frame(frame, bg='#2EC4B6', height=150)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="🔐 Verificación en dos pasos", font=('Segoe UI', 28, 'bold'),
                bg='#2EC4B6', fg='white').pack(pady=30)
        
        form = tk.Frame(frame, bg='white', padx=40, pady=30)
        form.place(relx=0.5, rely=0.4, anchor='center')
        
        tk.Label(form, text=f"Hola {nombre}", font=('Segoe UI', 16, 'bold'),
                bg='white', fg='#2d3748').pack()
        tk.Label(form, text="Ingresa el código de 6 dígitos enviado a tu email",
                font=('Segoe UI', 11), bg='white', fg='#718096').pack(pady=5)
        
        # ERROR 7: Anchura del entry incorrecta
        self.codigo_entry = tk.Entry(form, font=('Segoe UI', 18), width=6, justify='center')
        self.codigo_entry.pack(pady=20, ipady=10)
        
        btn_verificar = tk.Button(form, text="Verificar", font=('Segoe UI', 12, 'bold'),
                                  bg='#2EC4B6', fg='white', cursor='hand2', command=self.verificar_2fa)
        btn_verificar.pack(fill=tk.X, ipady=8)
        
        # ERROR 8: No hay botón para reenviar código
        # ERROR 9: No hay botón para volver al login
        
        self.codigo_entry.focus()
    
    def verificar_2fa(self):
        codigo = self.codigo_entry.get().strip()
        
        if not codigo:
            messagebox.showerror("Error", "Ingresa el código de verificación")
            return
        
        conexion = conectar_bd()
        if not conexion:
            messagebox.showerror("Error", "Error de conexión")
            return
        
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT codigo_2fa, codigo_2fa_expiracion FROM usuarios WHERE id = %s
        """, (self.temp_usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        
        if not resultado:
            messagebox.showerror("Error", "Usuario no encontrado")
            return
        
        codigo_guardado, expiracion = resultado
        
        if datetime.now() > expiracion:
            messagebox.showerror("Error", "El código ha expirado")
            return
        
        # ERROR 10: Comparación insegura (no usa constant time)
        if codigo != codigo_guardado:
            messagebox.showerror("Error", "Código incorrecto")
            return
        
        usuario = Usuario.obtener_por_id(self.temp_usuario_id)
        if usuario:
            self.on_success(usuario['id'], usuario['nombre'], usuario['tipo'])
    
    def ir_registro(self, tipo='cliente'):
        from views.registro_view import RegistroView
        RegistroView(self.parent, lambda: self.setup_ui(), tipo)
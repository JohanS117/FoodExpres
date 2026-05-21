"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: views/login_view.py
ERRORES: 10 errores intencionales
"""

import hmac
import logging
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from models.usuario import Usuario
from utils.security import generar_codigo_2fa, enviar_codigo_2fa, hash_password, validar_email
from config.database import conectar_bd, cerrar_conexion

class LoginView:
    
    def __init__(self, parent, on_success):
        self.parent = parent
        self.on_success = on_success
        self.temp_usuario_id = None
        self.temp_email = None
        self.temp_recovery_email = None
        self.intentos_2fa = 0
        self.setup_ui()
    
    def setup_ui(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.parent.configure(bg='#f8f9fa')
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        header = tk.Frame(main_frame, bg='#FF6B35', height=200)
        header.pack(fill=tk.X)
        
        # [LOG-01] Corregido: tamaño de fuente del título aumentado a 36pt
        tk.Label(header, text="🍔 FoodExpress", font=('Segoe UI', 36, 'bold'),
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
        
        # [LOG-02] Corregido: parámetros del comando del botón de registro
        tk.Button(form, text="¿No tienes cuenta? Regístrate", bg='white',
                 fg='#2EC4B6', font=('Segoe UI', 10), relief=tk.FLAT, cursor='hand2',
                 command=lambda: self.ir_registro('cliente')).pack()

        # [LOG-10] Agregado: opción para recuperar contraseña
        tk.Button(form, text="¿Olvidaste tu contraseña?", bg='white',
                 fg='#718096', font=('Segoe UI', 10), relief=tk.FLAT, cursor='hand2',
                 command=self.ir_recuperar_password).pack(pady=(4, 0))

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
        self.temp_email = email

        # [LOG-03] Corregido: se verifica existencia del usuario antes de generar código 2FA
        usuario_verificado = Usuario.obtener_por_id(self.temp_usuario_id)
        if not usuario_verificado:
            messagebox.showerror("Error", "No se pudo verificar el usuario")
            return

        codigo = generar_codigo_2fa()
        expiracion = datetime.now() + timedelta(minutes=5)
        
        conexion = conectar_bd()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        # [LOG-04] Corregido: manejo de errores en actualización de código 2FA
        try:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE usuarios SET codigo_2fa = %s, codigo_2fa_expiracion = %s
                WHERE id = %s
            """, (codigo, expiracion, usuario['id']))
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            logging.error("Error al guardar código 2FA para usuario %s: %s", usuario['id'], e)
            messagebox.showerror("Error", "No se pudo generar el código de verificación. Intenta de nuevo.")
            return
        finally:
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
        # [LOG-05] Corregido: ancho del campo de código 2FA cambiado de 6 a 10
        self.codigo_entry = tk.Entry(form, font=('Segoe UI', 18), width=10, justify='center')
        self.codigo_entry.pack(pady=20, ipady=10)
        
        btn_verificar = tk.Button(form, text="Verificar", font=('Segoe UI', 12, 'bold'),
                                  bg='#2EC4B6', fg='white', cursor='hand2', command=self.verificar_2fa)
        btn_verificar.pack(fill=tk.X, ipady=8)
        
        # [LOG-06] Agregado: botón para reenviar código 2FA
        btn_reenviar = tk.Button(form, text="Reenviar código", font=('Segoe UI', 10),
                                  bg='white', fg='#2EC4B6', relief=tk.FLAT, cursor='hand2',
                                  command=self.reenviar_codigo_2fa)
        btn_reenviar.pack(pady=(8, 0))

        tk.Frame(form, height=1, bg='#e2e8f0').pack(fill=tk.X, pady=(12, 4))

        # [LOG-07] Agregado: botón para volver al login desde pantalla 2FA
        btn_volver = tk.Button(form, text="← Volver al inicio de sesión", font=('Segoe UI', 10),
                                bg='white', fg='#718096', relief=tk.FLAT, cursor='hand2',
                                command=self.volver_al_login)
        btn_volver.pack()

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
        
        # [LOG-08] Corregido: comparación de código 2FA con hmac.compare_digest()
        if not hmac.compare_digest(str(codigo), str(codigo_guardado)):
            # [LOG-09] Corregido: límite de 3 intentos para código 2FA
            self.intentos_2fa += 1
            if self.intentos_2fa >= 3:
                self.bloquear_2fa()
            else:
                restantes = 3 - self.intentos_2fa
                messagebox.showerror("Error", f"Código incorrecto. Te quedan {restantes} intento(s).")
            return

        self.intentos_2fa = 0
        usuario = Usuario.obtener_por_id(self.temp_usuario_id)
        if usuario:
            self.on_success(usuario['id'], usuario['nombre'], usuario['tipo'])
    
    def reenviar_codigo_2fa(self):
        codigo = generar_codigo_2fa()
        expiracion = datetime.now() + timedelta(minutes=5)

        conexion = conectar_bd()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                UPDATE usuarios SET codigo_2fa = %s, codigo_2fa_expiracion = %s
                WHERE id = %s
            """, (codigo, expiracion, self.temp_usuario_id))
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            logging.error("Error al reenviar código 2FA para usuario %s: %s", self.temp_usuario_id, e)
            messagebox.showerror("Error", "No se pudo reenviar el código. Intenta de nuevo.")
            return
        finally:
            cerrar_conexion(conexion)

        enviar_codigo_2fa(self.temp_email, codigo)
        messagebox.showinfo("Código enviado", "Se ha enviado un nuevo código a tu email.")

    def bloquear_2fa(self):
        messagebox.showerror(
            "Acceso bloqueado",
            "Has superado el número máximo de intentos. El código ha sido invalidado."
        )
        self.volver_al_login()

    def volver_al_login(self):
        if self.temp_usuario_id:
            conexion = conectar_bd()
            if conexion:
                try:
                    cursor = conexion.cursor()
                    cursor.execute("""
                        UPDATE usuarios SET codigo_2fa = NULL, codigo_2fa_expiracion = NULL
                        WHERE id = %s
                    """, (self.temp_usuario_id,))
                    conexion.commit()
                except Exception as e:
                    logging.error("Error al invalidar código 2FA para usuario %s: %s", self.temp_usuario_id, e)
                finally:
                    cerrar_conexion(conexion)

        self.temp_usuario_id = None
        self.temp_email = None
        self.temp_recovery_email = None
        self.intentos_2fa = 0
        self.setup_ui()

    def ir_recuperar_password(self):
        self.temp_recovery_email = None
        self.mostrar_recuperacion_password()

    def mostrar_recuperacion_password(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.parent, bg='#f8f9fa')
        frame.pack(expand=True, fill=tk.BOTH)

        header = tk.Frame(frame, bg='#FF6B35', height=150)
        header.pack(fill=tk.X)

        tk.Label(header, text="🔑 Recuperar contraseña", font=('Segoe UI', 28, 'bold'),
                bg='#FF6B35', fg='white').pack(pady=30)

        form = tk.Frame(frame, bg='white', padx=40, pady=30)
        form.place(relx=0.5, rely=0.4, anchor='center')

        tk.Label(form, text="Ingresa tu email registrado", font=('Segoe UI', 13, 'bold'),
                bg='white', fg='#2d3748').pack(pady=(0, 5))
        tk.Label(form, text="Te enviaremos un código para restablecer tu contraseña",
                font=('Segoe UI', 10), bg='white', fg='#718096').pack(pady=(0, 15))

        email_entry = tk.Entry(form, font=('Segoe UI', 12), width=30)
        email_entry.pack(ipady=8)
        email_entry.focus()

        tk.Button(form, text="Enviar código", font=('Segoe UI', 12, 'bold'),
                  bg='#FF6B35', fg='white', cursor='hand2',
                  command=lambda: self.enviar_codigo_recuperacion(email_entry)).pack(
                      fill=tk.X, ipady=8, pady=(20, 0))

        tk.Frame(form, height=1, bg='#e2e8f0').pack(fill=tk.X, pady=(12, 4))

        tk.Button(form, text="← Volver al inicio de sesión", font=('Segoe UI', 10),
                  bg='white', fg='#718096', relief=tk.FLAT, cursor='hand2',
                  command=self.setup_ui).pack()

    def enviar_codigo_recuperacion(self, email_entry):
        email = email_entry.get().strip()

        if not email:
            messagebox.showerror("Error", "Ingresa tu email")
            return

        if not validar_email(email):
            messagebox.showerror("Error", "El formato del email no es válido")
            return

        conexion = conectar_bd()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT id FROM usuarios WHERE email = %s AND activo = 1",
                (email,)
            )
            resultado = cursor.fetchone()

            if not resultado:
                messagebox.showerror("Error", "No existe una cuenta registrada con ese email")
                return

            codigo = generar_codigo_2fa()
            expiracion = datetime.now() + timedelta(minutes=15)

            cursor.execute("""
                UPDATE usuarios SET codigo_2fa = %s, codigo_2fa_expiracion = %s
                WHERE id = %s
            """, (codigo, expiracion, resultado[0]))
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            logging.error("Error al generar código de recuperación para %s: %s", email, e)
            messagebox.showerror("Error", "No se pudo generar el código. Intenta de nuevo.")
            return
        finally:
            cerrar_conexion(conexion)

        self.temp_recovery_email = email
        enviar_codigo_2fa(email, codigo)
        messagebox.showinfo("Código enviado", f"Se ha enviado un código de recuperación a {email}.")
        self.mostrar_nueva_password()

    def mostrar_nueva_password(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.parent, bg='#f8f9fa')
        frame.pack(expand=True, fill=tk.BOTH)

        header = tk.Frame(frame, bg='#FF6B35', height=150)
        header.pack(fill=tk.X)

        tk.Label(header, text="🔑 Nueva contraseña", font=('Segoe UI', 28, 'bold'),
                bg='#FF6B35', fg='white').pack(pady=30)

        form = tk.Frame(frame, bg='white', padx=40, pady=30)
        form.place(relx=0.5, rely=0.4, anchor='center')

        tk.Label(form, text="Código de recuperación", font=('Segoe UI', 11),
                bg='white', anchor='w').pack(fill=tk.X)
        codigo_entry = tk.Entry(form, font=('Segoe UI', 12), width=20, justify='center')
        codigo_entry.pack(ipady=8, pady=(5, 15))

        tk.Label(form, text="Nueva contraseña", font=('Segoe UI', 11),
                bg='white', anchor='w').pack(fill=tk.X)
        nueva_entry = tk.Entry(form, font=('Segoe UI', 12), width=30, show="*")
        nueva_entry.pack(ipady=8, pady=(5, 15))

        tk.Label(form, text="Confirmar contraseña", font=('Segoe UI', 11),
                bg='white', anchor='w').pack(fill=tk.X)
        confirmar_entry = tk.Entry(form, font=('Segoe UI', 12), width=30, show="*")
        confirmar_entry.pack(ipady=8, pady=(5, 20))

        tk.Button(form, text="Restablecer contraseña", font=('Segoe UI', 12, 'bold'),
                  bg='#FF6B35', fg='white', cursor='hand2',
                  command=lambda: self.confirmar_nueva_password(
                      codigo_entry, nueva_entry, confirmar_entry)).pack(fill=tk.X, ipady=8)

        tk.Frame(form, height=1, bg='#e2e8f0').pack(fill=tk.X, pady=(12, 4))

        tk.Button(form, text="← Volver al inicio de sesión", font=('Segoe UI', 10),
                  bg='white', fg='#718096', relief=tk.FLAT, cursor='hand2',
                  command=self.setup_ui).pack()

        codigo_entry.focus()

    def confirmar_nueva_password(self, codigo_entry, nueva_entry, confirmar_entry):
        codigo = codigo_entry.get().strip()
        nueva = nueva_entry.get().strip()
        confirmar = confirmar_entry.get().strip()

        if not codigo or not nueva or not confirmar:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if nueva != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        if len(nueva) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return

        conexion = conectar_bd()
        if not conexion:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        try:
            cursor = conexion.cursor()
            cursor.execute("""
                SELECT id, codigo_2fa, codigo_2fa_expiracion
                FROM usuarios WHERE email = %s AND activo = 1
            """, (self.temp_recovery_email,))
            resultado = cursor.fetchone()

            if not resultado:
                messagebox.showerror("Error", "Usuario no encontrado")
                return

            usuario_id, codigo_guardado, expiracion = resultado

            if datetime.now() > expiracion:
                messagebox.showerror("Error", "El código ha expirado. Solicita uno nuevo.")
                return

            if not hmac.compare_digest(str(codigo), str(codigo_guardado)):
                messagebox.showerror("Error", "Código de recuperación incorrecto")
                return

            cursor.execute("""
                UPDATE usuarios SET password = %s, codigo_2fa = NULL, codigo_2fa_expiracion = NULL
                WHERE id = %s
            """, (hash_password(nueva), usuario_id))
            conexion.commit()
        except Exception as e:
            conexion.rollback()
            logging.error("Error al restablecer contraseña para %s: %s", self.temp_recovery_email, e)
            messagebox.showerror("Error", "No se pudo actualizar la contraseña. Intenta de nuevo.")
            return
        finally:
            cerrar_conexion(conexion)

        self.temp_recovery_email = None
        messagebox.showinfo("Éxito", "Tu contraseña ha sido actualizada. Ya puedes iniciar sesión.")
        self.setup_ui()

    def ir_registro(self, tipo='cliente'):
        from views.registro_view import RegistroView
        RegistroView(self.parent, self.setup_ui, tipo)
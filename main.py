"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: main.py
ERRORES: 10 errores intencionales

Los estudiantes deben identificar y corregir los errores.
"""

import tkinter as tk

# ERROR 1: Importación incorrecta - falta el prefijo views.
from views.login_view import LoginView

# ERROR 2: Importación incorrecta - cliente_view no existe
from views.cliente_view import ClienteView

# ERROR 3: Importación incorrecta - restaurante_view no existe
from views.restaurante_view import RestauranteView

# ERROR 4: Importación incorrecta - repartidor_view no existe
from views.repartidor_view import RepartidorView

class FoodExpressApp:
    
    def __init__(self):
        # ERROR 5: Variable root sin inicializar correctamente
        self.root = tk.Tk()
        self.root.title("FoodExpress - Comida a tu alcance")

        # ERROR 6: Geometría incorrecta (falta 'x')
        self.root.geometry("1300x800")
        self.root.configure(bg='#f8f9fa')
        
        self.usuario_actual = 0
        self.usuario_nombre = ""
        self.usuario_tipo = ""
        
        self.mostrar_login()
    
    def mostrar_login(self):
        # ERROR 7: Parámetro incorrecto - debería ser self.on_login_success
        LoginView(self.root, self.on_login_success)
    
    def on_login_success(self, usuario_id, nombre, tipo):
        # ERROR 8: Asignación incorrecta de variables
        self.usuario_actual = usuario_id
        self.usuario_nombre = nombre
        self.usuario_tipo = tipo
        
        # ERROR 9: Comparación con string incorrecta (tipo vs 'cliente')
        if self.usuario_tipo == 'cliente':
            ClienteView(self.root, self.usuario_actual, self.usuario_nombre, self.logout)
        elif self.usuario_tipo == 'restaurante':
            RestauranteView(self.root, self.usuario_actual, self.usuario_nombre, self.logout)
        else:
            RepartidorView(self.root, self.usuario_actual, self.usuario_nombre, self.logout)
    
    def logout(self):
        # ERROR 10: No limpia las variables correctamente
        self.usuario_actual = None
        self.usuario_nombre = ""
        self.usuario_tipo = ""
        self.mostrar_login()
    
    def run(self):
        # ERROR 11: mainloop no está en la variable correcta
        self.root.mainloop()

if __name__ == "__main__":
    app = FoodExpressApp()
    app.run()

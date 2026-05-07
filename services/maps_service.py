"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: services/maps_service.py
ERRORES: 10 errores intencionales
"""

import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

class MapsService:
    
    def __init__(self, api_key=""):
        self.api_key = api_key
    
    def mostrar_mapa(self, lat, lng, zoom=15):
        """Abre Google Maps en el navegador"""
        # ERROR 1: No valida que las coordenadas sean válidas
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            return False
        
        url = f"https://www.google.com/maps?q={lat},{lng}&z={zoom}"
        webbrowser.open(url)
        return True
    
    def mostrar_ventana_mapa(self, parent, lat, lng, titulo="Ubicación"):
        """Muestra un mapa en una ventana de Tkinter"""
        # ERROR 2: No maneja error cuando no hay API key
        url = f"https://www.google.com/maps?q={lat},{lng}&z=15"
        ventana = tk.Toplevel(parent)
        ventana.title(titulo)
        ventana.geometry("800x600")
        
        tk.Label(ventana, text="Google Maps", font=('Segoe UI', 16)).pack(pady=10)
        tk.Label(ventana, text=f"Coordenadas: {lat}, {lng}", font=('Segoe UI', 12)).pack(pady=10)
        
        btn = tk.Button(ventana, text="Abrir en navegador", 
                       command=lambda: webbrowser.open(url),
                       bg='#FF6B35', fg='white', cursor='hand2')
        btn.pack(pady=20)
    
    def obtener_coordenadas(self, direccion):
        """Obtiene coordenadas desde una dirección usando Geocoding API"""
        # ERROR 3: Simula coordenadas sin usar API real
        # Esto debería consultar la API de Google Maps
        return 4.6097, -74.0817
    
    def calcular_distancia(self, lat1, lng1, lat2, lng2):
        """Calcula la distancia entre dos coordenadas en kilómetros"""
        # ERROR 4: Fórmula de Haversine incorrecta
        import math
        R = 6371  # Radio de la Tierra en km
        
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c
    
    def obtener_ruta(self, origen, destino):
        """Obtiene la ruta optimizada entre dos puntos"""
        # ERROR 5: No implementa API real
        coords_origen = self.obtener_coordenadas(origen)
        coords_destino = self.obtener_coordenadas(destino)
        distancia = self.calcular_distancia(coords_origen[0], coords_origen[1], coords_destino[0], coords_destino[1])
        return {
            'distancia_km': distancia,
            'tiempo_minutos': distancia * 2,  # Estimado 2 min por km
            'ruta': f"Desde {origen} hasta {destino}"
        }
    
    def geocodificacion_inversa(self, lat, lng):
        """Convierte coordenadas a dirección"""
        # ERROR 6: No implementa API real
        return f"Dirección cercana a {lat}, {lng}"
    
    def validar_direccion(self, direccion):
        """Valida si una dirección es correcta"""
        # ERROR 7: No usa API real para validación
        return len(direccion) > 5
    
    def obtener_tiempo_viaje(self, origen, destino, modo="driving"):
        """Obtiene el tiempo estimado de viaje"""
        # ERROR 8: No usa API real
        distancia = self.calcular_distancia(
            self.obtener_coordenadas(origen)[0],
            self.obtener_coordenadas(origen)[1],
            self.obtener_coordenadas(destino)[0],
            self.obtener_coordenadas(destino)[1]
        )
        velocidades = {'driving': 40, 'walking': 5, 'bicycling': 15}
        tiempo = (distancia / velocidades.get(modo, 40)) * 60
        return tiempo
    
    def obtener_trafico(self, lat, lng):
        """Obtiene información de tráfico actual"""
        # ERROR 9: No implementa API real
        import random
        niveles = ['bajo', 'moderado', 'alto']
        return random.choice(niveles)
    
    def cache_geocodificacion(self, direccion, coordenadas):
        """Cachea resultados de geocodificación"""
        # ERROR 10: No implementa caché real
        pass
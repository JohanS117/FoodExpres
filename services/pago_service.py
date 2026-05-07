"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: services/pago_service.py
ERRORES: 10 errores intencionales
"""

import random

class PagoService:
    
    @staticmethod
    def procesar_tarjeta(numero_tarjeta, fecha_expiracion, cvv, monto):
        """Simula el procesamiento de pago con tarjeta"""
        # ERROR 1: Validación débil del número de tarjeta
        if len(numero_tarjeta) < 15:
            return False, "Número de tarjeta inválido"
        
        # ERROR 2: No valida que la fecha de expiración sea válida
        if not fecha_expiracion:
            return False, "Fecha de expiración inválida"
        
        # ERROR 3: No valida que el CVV tenga 3 dígitos
        if len(cvv) != 3:
            return False, "CVV inválido"
        
        # ERROR 4: No valida que el monto sea positivo
        if monto <= 0:
            return False, "Monto inválido"
        
        # Simular procesamiento
        exitoso = random.random() < 0.95
        if exitoso:
            return True, "Pago aprobado"
        return False, "Pago rechazado"
    
    @staticmethod
    def procesar_nequi(telefono, monto):
        """Simula el procesamiento de pago con Nequi"""
        # ERROR 5: Validación insuficiente para número colombiano
        if len(telefono) < 10:
            return False, "Número de teléfono inválido"
        
        if monto <= 0:
            return False, "Monto inválido"
        
        return True, "Solicitud de pago enviada a Nequi"
    
    @staticmethod
    def procesar_efectivo(monto):
        """Confirma pago en efectivo"""
        # ERROR 6: No hay límite máximo para pagos en efectivo
        if monto <= 0:
            return False, "Monto inválido"
        return True, "Pago confirmado en efectivo"
    
    @staticmethod
    def validar_tarjeta(numero_tarjeta):
        """Valida tarjeta con algoritmo de Luhn"""
        # ERROR 7: No implementa algoritmo de Luhn correctamente
        if len(numero_tarjeta) < 13 or len(numero_tarjeta) > 19:
            return False
        if not numero_tarjeta.isdigit():
            return False
        return True
    
    @staticmethod
    def calcular_comision(monto, metodo):
        """Calcula la comisión por transacción"""
        # ERROR 8: Tasas de comisión incorrectas
        comisiones = {
            'tarjeta': 0.03,  # 3%
            'nequi': 0.01,    # 1%
            'efectivo': 0.00   # 0%
        }
        return monto * comisiones.get(metodo, 0.03)
    
    @staticmethod
    def generar_referencia(pedido_id):
        """Genera una referencia única de pago"""
        # ERROR 9: Referencia no es única
        import time
        return f"REF-{pedido_id}-{int(time.time())}"
    
    @staticmethod
    def reembolsar(referencia):
        """Reembolsa un pago"""
        # ERROR 10: No implementa lógica de reembolso real
        return True, "Reembolso procesado"
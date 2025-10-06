#!/usr/bin/env python
"""
Script para crear alertas de stock de prueba
"""
import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventario.models import Producto, AlertaStock


def crear_alertas_prueba():
    print("Creando alertas de stock de prueba...")
    
    # Obtener algunos productos para crear alertas
    productos_con_stock_bajo = [
        'AM004',  # Zapatillas desechables
        'BB001',  # Vino Tinto Reserva 
        'LM002',  # Desinfectante Multiuso
        'TX002',  # Sábanas Matrimoniales
    ]
    
    for codigo in productos_con_stock_bajo:
        try:
            producto = Producto.objects.get(codigo=codigo)
            
            # Verificar si ya existe una alerta activa para este producto
            alerta_existente = AlertaStock.objects.filter(
                producto=producto,
                estado='ACTIVA'
            ).exists()
            
            if not alerta_existente:
                # Crear alerta
                alerta = AlertaStock.objects.create(
                    producto=producto,
                    stock_actual=producto.stock_total(),
                    stock_minimo=producto.stock_minimo,
                    estado='ACTIVA'
                )
                
                print(f"  ✓ Alerta creada para: {producto.nombre} (Stock: {alerta.stock_actual}, Mínimo: {alerta.stock_minimo})")
            else:
                print(f"  - Alerta ya existe para: {producto.nombre}")
                
        except Producto.DoesNotExist:
            print(f"  ✗ Producto no encontrado: {codigo}")
    
    total_alertas = AlertaStock.objects.filter(estado='ACTIVA').count()
    print(f"\n✅ Proceso completado. Total de alertas activas: {total_alertas}")


if __name__ == '__main__':
    crear_alertas_prueba()
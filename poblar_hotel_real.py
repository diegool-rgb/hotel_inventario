#!/usr/bin/env python
"""
Script para poblar el sistema con datos reales basados en la entrevista del hotel.
Refleja los problemas y necesidades específicas mencionadas por la administradora.
"""

import os
import django

# Configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Categoria, Producto, Area, Stock, Movimiento, AlertaStock
from usuarios.models import PerfilUsuario
from datetime import datetime, timedelta
import random

def crear_datos_reales_hotel():
    print("🏨 Creando datos reales basados en la entrevista del hotel...")
    
    # 1. Crear áreas específicas del hotel mencionadas en la entrevista
    print("\n📍 Creando áreas del hotel...")
    areas_hotel = [
        ("Housekeeping Central", "Área principal de limpieza y amenities"),
        ("Habitaciones Piso 1", "Frigobar y amenities habitaciones piso 1"),
        ("Habitaciones Piso 2", "Frigobar y amenities habitaciones piso 2"),
        ("Habitaciones Piso 3", "Frigobar y amenities habitaciones piso 3"),
        ("Restaurante Principal", "Área del restaurante - control garzones"),
        ("Bar del Hotel", "Área del bar - bebidas y snacks"),
        ("Cocina Principal", "Cocina - control jefa A&B"),
        ("Bodega Abarrotes", "Almacén principal de abarrotes"),
        ("Bodega Limpieza", "Productos de limpieza y mantenimiento"),
        ("Recepción", "Área de recepción y administración")
    ]
    
    for nombre, descripcion in areas_hotel:
        area, created = Area.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion, 'activo': True, 'tipo': 'BODEGA'}
        )
        if created:
            print(f"  ✓ {nombre}")
    
    # 2. Crear categorías específicas del hotel
    print("\n🏷️ Creando categorías basadas en la operación real...")
    categorias_hotel = [
        ("Amenities Baño", "Shampoo, jabón, toallas, papel higiénico", True),
        ("Frigobar", "Bebidas, snacks, agua para habitaciones", True),
        ("Productos Limpieza", "Detergentes, desinfectantes, escobas", True),
        ("Mantenimiento", "Herramientas, repuestos, materiales", True),
        ("Cocina - Abarrotes", "Ingredientes, condimentos, conservas", True),
        ("Cocina - Frescos", "Carnes, verduras, lácteos, pan", True),
        ("Bebidas Restaurante", "Vinos, cervezas, jugos, gaseosas", True),
        ("Lencería", "Sábanas, toallas, manteles, servilletas", True),
        ("Papelería", "Facturas, papel, bolígrafos, folders", True),
        ("Equipos", "Aspiradoras, secadores, equipos cocina", False)
    ]
    
    for nombre, descripcion, activa in categorias_hotel:
        categoria, created = Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion, 'activo': activa}
        )
        if created:
            print(f"  ✓ {nombre}")
    
    # 3. Crear productos específicos mencionados en operaciones reales
    print("\n📦 Creando productos de operación diaria...")
    
    productos_reales = [
        # Amenities Baño
        ("AME001", "Shampoo individual 30ml", "Amenities Baño", "UNI", 50, 1200),
        ("AME002", "Acondicionador individual 30ml", "Amenities Baño", "UNI", 50, 1000),
        ("AME003", "Jabón corporal individual", "Amenities Baño", "UNI", 100, 800),
        ("AME004", "Papel higiénico premium", "Amenities Baño", "UNI", 200, 2400),
        ("AME005", "Toallas de baño blancas", "Amenities Baño", "UNI", 20, 120),
        
        # Frigobar
        ("FRG001", "Agua mineral 500ml", "Frigobar", "UNI", 100, 500),
        ("FRG002", "Coca Cola 350ml", "Frigobar", "UNI", 50, 200),
        ("FRG003", "Cerveza nacional 330ml", "Frigobar", "UNI", 30, 150),
        ("FRG004", "Snack papas fritas", "Frigobar", "UNI", 25, 80),
        ("FRG005", "Maní salado pequeño", "Frigobar", "UNI", 20, 60),
        
        # Productos Limpieza
        ("LMP001", "Desinfectante multiuso 1L", "Productos Limpieza", "UNI", 10, 25),
        ("LMP002", "Detergente para pisos 1L", "Productos Limpieza", "UNI", 8, 20),
        ("LMP003", "Papel toalla industrial", "Productos Limpieza", "UNI", 50, 200),
        ("LMP004", "Bolsas basura grandes", "Productos Limpieza", "UNI", 100, 500),
        ("LMP005", "Escobas industriales", "Productos Limpieza", "UNI", 5, 8),
        
        # Cocina - Abarrotes
        ("COC001", "Arroz premium 5kg", "Cocina - Abarrotes", "KG", 50, 200),
        ("COC002", "Aceite vegetal 1L", "Cocina - Abarrotes", "UNI", 12, 24),
        ("COC003", "Sal fina 1kg", "Cocina - Abarrotes", "KG", 20, 50),
        ("COC004", "Azúcar blanca 1kg", "Cocina - Abarrotes", "KG", 25, 80),
        ("COC005", "Fideos spaghetti 500g", "Cocina - Abarrotes", "UNI", 30, 100),
        
        # Bebidas Restaurante
        ("BEB001", "Vino tinto reserva", "Bebidas Restaurante", "UNI", 6, 24),
        ("BEB002", "Cerveza artesanal", "Bebidas Restaurante", "UNI", 20, 100),
        ("BEB003", "Jugo naranja natural 1L", "Bebidas Restaurante", "UNI", 10, 30),
        ("BEB004", "Agua con gas 500ml", "Bebidas Restaurante", "UNI", 25, 120),
        
        # Lencería
        ("LEN001", "Sábanas matrimoniales blancas", "Lencería", "UNI", 15, 60),
        ("LEN002", "Fundas almohada blancas", "Lencería", "UNI", 30, 120),
        ("LEN003", "Manteles restaurante", "Lencería", "UNI", 10, 25),
        ("LEN004", "Servilletas de tela", "Lencería", "UNI", 50, 200),
    ]
    
    for codigo, nombre, categoria_nombre, unidad, stock_min, precio in productos_reales:
        categoria = Categoria.objects.get(nombre=categoria_nombre)
        producto, created = Producto.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre,
                'categoria': categoria,
                'unidad_medida': unidad,
                'stock_minimo': stock_min,
                'precio_unitario': precio,
                'activo': True
            }
        )
        if created:
            print(f"  ✓ {codigo} - {nombre}")
    
    # 4. Crear stock realista en las áreas
    print("\n📊 Distribuyendo stock por áreas...")
    
    # Distribución específica por tipo de producto y área
    distribuciones = {
        "Amenities Baño": ["Housekeeping Central", "Habitaciones Piso 1", "Habitaciones Piso 2", "Habitaciones Piso 3"],
        "Frigobar": ["Habitaciones Piso 1", "Habitaciones Piso 2", "Habitaciones Piso 3", "Bar del Hotel"],
        "Productos Limpieza": ["Housekeeping Central", "Bodega Limpieza"],
        "Cocina - Abarrotes": ["Cocina Principal", "Bodega Abarrotes"],
        "Bebidas Restaurante": ["Restaurante Principal", "Bar del Hotel"],
        "Lencería": ["Housekeeping Central"],
    }
    
    for categoria_nombre, areas_nombres in distribuciones.items():
        categoria = Categoria.objects.get(nombre=categoria_nombre)
        productos = Producto.objects.filter(categoria=categoria)
        
        for producto in productos:
            for area_nombre in areas_nombres:
                area = Area.objects.get(nombre=area_nombre)
                
                # Cantidad aleatoria pero realista
                if "Habitaciones" in area_nombre:
                    cantidad_base = int(producto.stock_minimo) // 4  # Menos stock en habitaciones
                else:
                    cantidad_base = int(producto.stock_minimo) * random.randint(1, 3)
                
                # Simular algunos productos con stock bajo (problema real mencionado)
                if random.random() < 0.3:  # 30% probabilidad de stock bajo
                    cantidad = random.randint(1, int(producto.stock_minimo) // 2)
                else:
                    cantidad = cantidad_base
                
                stock, created = Stock.objects.get_or_create(
                    producto=producto,
                    area=area,
                    defaults={'cantidad': cantidad}
                )
                if created:
                    print(f"  ✓ {producto.codigo} en {area.nombre}: {cantidad}")
    
    # 5. Crear alertas automáticas para stock bajo
    print("\n🚨 Generando alertas de stock bajo...")
    
    productos = Producto.objects.all()
    alertas_creadas = 0
    
    for producto in productos:
        stock_total = sum(stock.cantidad for stock in producto.stocks.all())
        
        if stock_total <= int(producto.stock_minimo):
            alerta, created = AlertaStock.objects.get_or_create(
                producto=producto,
                estado='ACTIVA',
                defaults={
                    'stock_actual': stock_total,
                    'stock_minimo': producto.stock_minimo,
                    'observaciones': f'Stock crítico: {stock_total} unidades disponibles (mínimo: {producto.stock_minimo})'
                }
            )
            if created:
                alertas_creadas += 1
                print(f"  ⚠️ Alerta creada para {producto.nombre}")
    
    print(f"\n✅ Proceso completado:")
    print(f"   • {Area.objects.count()} áreas del hotel")
    print(f"   • {Categoria.objects.count()} categorías de productos")
    print(f"   • {Producto.objects.count()} productos de operación real")
    print(f"   • {Stock.objects.count()} registros de stock distribuido")
    print(f"   • {alertas_creadas} alertas de stock bajo")
    
    print(f"\n🎯 Datos basados en insights de la entrevista:")
    print(f"   • Áreas específicas: Housekeeping, Restaurante, Cocina, Habitaciones")
    print(f"   • Productos reales: Amenities, Frigobar, Limpieza, Abarrotes")
    print(f"   • Simulación de stock bajo para prevenir pedidos de emergencia")
    print(f"   • Control por roles: Administradora, Housekeeping, Garzones, Jefa A&B")

if __name__ == "__main__":
    crear_datos_reales_hotel()
#!/usr/bin/env python
"""
Script para poblar la base de datos con proveedores ficticios de Chile
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventario.models import Proveedor

def crear_proveedores_chile():
    """Crear proveedores ficticios de Chile"""
    
    proveedores_data = [
        {
            'nombre': 'Distribuidora Central S.A.',
            'contacto': 'María González',
            'telefono': '+56-2-2234-5678',
            'email': 'ventas@distribuidoracentral.cl',
            'direccion': 'Av. Libertador Bernardo O\'Higgins 1234, Santiago',
            'rut': '76.123.456-7'
        },
        {
            'nombre': 'Comercial Hotelera Ltda.',
            'contacto': 'Carlos Mendoza',
            'telefono': '+56-2-2876-5432',
            'email': 'comercial@hotelera.cl',
            'direccion': 'Calle Huérfanos 567, Santiago Centro',
            'rut': '89.234.567-8'
        },
        {
            'nombre': 'Abastecedora del Sur',
            'contacto': 'Ana Rodríguez',
            'telefono': '+56-41-2345-678',
            'email': 'pedidos@abastecedoradelsur.cl',
            'direccion': 'Av. Pedro Montt 890, Valparaíso',
            'rut': '92.345.678-9'
        },
        {
            'nombre': 'Suministros Norte S.A.',
            'contacto': 'Pedro Martínez',
            'telefono': '+56-55-2567-890',
            'email': 'ventas@suministrosnorte.cl',
            'direccion': 'Av. Arturo Prat 432, Antofagasta',
            'rut': '85.456.789-0'
        },
        {
            'nombre': 'Importadora Pacific',
            'contacto': 'Luis Silva',
            'telefono': '+56-2-2654-3210',
            'email': 'importaciones@pacific.cl',
            'direccion': 'Las Condes 2456, Las Condes, Santiago',
            'rut': '78.567.890-1'
        },
        {
            'nombre': 'Mayorista El Rápido',
            'contacto': 'Sandra Torres',
            'telefono': '+56-32-2123-456',
            'email': 'mayorista@elrapido.cl',
            'direccion': 'Av. Brasil 123, Viña del Mar',
            'rut': '91.678.901-2'
        },
        {
            'nombre': 'Tecnología Hotelera Chile',
            'contacto': 'Roberto Fernández',
            'telefono': '+56-2-2789-0123',
            'email': 'soporte@techhotel.cl',
            'direccion': 'Providencia 789, Providencia, Santiago',
            'rut': '84.789.012-3'
        },
        {
            'nombre': 'Lavandería Industrial ChileLimp',
            'contacto': 'Carmen Morales',
            'telefono': '+56-2-2890-1234',
            'email': 'servicios@chilelimp.cl',
            'direccion': 'Av. Independencia 345, Independencia, Santiago',
            'rut': '87.890.123-4'
        }
    ]
    
    print("Creando proveedores para Chile...")
    
    for proveedor_data in proveedores_data:
        # Verificar si ya existe
        if not Proveedor.objects.filter(rut=proveedor_data['rut']).exists():
            proveedor = Proveedor.objects.create(**proveedor_data)
            print(f"✓ Creado: {proveedor.nombre}")
        else:
            print(f"- Ya existe: {proveedor_data['nombre']}")
    
    print(f"\n✅ Proceso completado. Total proveedores activos: {Proveedor.objects.filter(activo=True).count()}")

if __name__ == '__main__':
    crear_proveedores_chile()
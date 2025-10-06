#!/usr/bin/env python
"""
Script para cargar datos iniciales del sistema de inventario hotelero.
Ejecutar con: python manage.py shell < data_inicial.py
"""
import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Categoria, Area, Producto, Stock
from pedidos.models import Proveedor
from usuarios.models import PerfilUsuario


def crear_datos_iniciales():
    print("Creando datos iniciales...")
    
    # 1. Crear categorías
    categorias_data = [
        {'nombre': 'Amenities', 'descripcion': 'Productos de cortesía para habitaciones'},
        {'nombre': 'Bebidas Alcohólicas', 'descripcion': 'Vinos, licores, cervezas'},
        {'nombre': 'Bebidas No Alcohólicas', 'descripcion': 'Jugos, gaseosas, agua'},
        {'nombre': 'Alimentos Frescos', 'descripcion': 'Carnes, pescados, verduras'},
        {'nombre': 'Alimentos Secos', 'descripcion': 'Arroz, pasta, legumbres'},
        {'nombre': 'Productos de Limpieza', 'descripcion': 'Detergentes, desinfectantes'},
        {'nombre': 'Suministros de Oficina', 'descripcion': 'Papel, bolígrafos, formularios'},
        {'nombre': 'Textiles', 'descripcion': 'Toallas, sábanas, manteles'},
    ]
    
    for cat_data in categorias_data:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        if created:
            print(f"  ✓ Categoría creada: {categoria.nombre}")
    
    # 2. Crear áreas
    areas_data = [
        {'nombre': 'Bodega Principal', 'tipo': 'BODEGA', 'descripcion': 'Almacén general del hotel'},
        {'nombre': 'Cocina', 'tipo': 'COCINA', 'descripcion': 'Área de preparación de alimentos'},
        {'nombre': 'Bar', 'tipo': 'BAR', 'descripcion': 'Bar del hotel'},
        {'nombre': 'Habitaciones Piso 1', 'tipo': 'HABITACION', 'descripcion': 'Frigo-bar habitaciones piso 1'},
        {'nombre': 'Habitaciones Piso 2', 'tipo': 'HABITACION', 'descripcion': 'Frigo-bar habitaciones piso 2'},
        {'nombre': 'Housekeeping', 'tipo': 'LIMPIEZA', 'descripcion': 'Área de limpieza y mantenimiento'},
        {'nombre': 'Recepción', 'tipo': 'RECEPCION', 'descripcion': 'Área de recepción'},
    ]
    
    for area_data in areas_data:
        area, created = Area.objects.get_or_create(
            nombre=area_data['nombre'],
            defaults=area_data
        )
        if created:
            print(f"  ✓ Área creada: {area.nombre}")
    
    # 3. Crear algunos productos de ejemplo
    productos_data = [
        # Amenities
        {'codigo': 'AM001', 'nombre': 'Shampoo 30ml', 'categoria': 'Amenities', 'unidad': 'UN', 'stock_min': 100, 'precio': 350},
        {'codigo': 'AM002', 'nombre': 'Acondicionador 30ml', 'categoria': 'Amenities', 'unidad': 'UN', 'stock_min': 100, 'precio': 350},
        {'codigo': 'AM003', 'nombre': 'Jabón de tocador', 'categoria': 'Amenities', 'unidad': 'UN', 'stock_min': 200, 'precio': 250},
        {'codigo': 'AM004', 'nombre': 'Zapatillas desechables', 'categoria': 'Amenities', 'unidad': 'PAR', 'stock_min': 50, 'precio': 800},
        
        # Bebidas
        {'codigo': 'BB001', 'nombre': 'Vino Tinto Reserva', 'categoria': 'Bebidas Alcohólicas', 'unidad': 'BOT', 'stock_min': 12, 'precio': 8500},
        {'codigo': 'BB002', 'nombre': 'Cerveza Nacional', 'categoria': 'Bebidas Alcohólicas', 'unidad': 'BOT', 'stock_min': 24, 'precio': 1200},
        {'codigo': 'BN001', 'nombre': 'Agua Mineral 500ml', 'categoria': 'Bebidas No Alcohólicas', 'unidad': 'BOT', 'stock_min': 48, 'precio': 800},
        {'codigo': 'BN002', 'nombre': 'Jugo de Naranja 1L', 'categoria': 'Bebidas No Alcohólicas', 'unidad': 'BOT', 'stock_min': 12, 'precio': 1500},
        
        # Alimentos
        {'codigo': 'AF001', 'nombre': 'Salmón Fresco', 'categoria': 'Alimentos Frescos', 'unidad': 'KG', 'stock_min': 5, 'precio': 12000},
        {'codigo': 'AF002', 'nombre': 'Verduras Mixtas', 'categoria': 'Alimentos Frescos', 'unidad': 'KG', 'stock_min': 10, 'precio': 2500},
        {'codigo': 'AS001', 'nombre': 'Arroz Grano Largo', 'categoria': 'Alimentos Secos', 'unidad': 'KG', 'stock_min': 25, 'precio': 1200},
        {'codigo': 'AS002', 'nombre': 'Pasta Italiana', 'categoria': 'Alimentos Secos', 'unidad': 'KG', 'stock_min': 15, 'precio': 2800},
        
        # Limpieza
        {'codigo': 'LM001', 'nombre': 'Detergente Líquido 5L', 'categoria': 'Productos de Limpieza', 'unidad': 'UN', 'stock_min': 6, 'precio': 3500},
        {'codigo': 'LM002', 'nombre': 'Desinfectante Multiuso', 'categoria': 'Productos de Limpieza', 'unidad': 'LT', 'stock_min': 10, 'precio': 2200},
        
        # Textiles
        {'codigo': 'TX001', 'nombre': 'Toalla de Baño Blanca', 'categoria': 'Textiles', 'unidad': 'UN', 'stock_min': 30, 'precio': 4500},
        {'codigo': 'TX002', 'nombre': 'Sábanas Matrimoniales', 'categoria': 'Textiles', 'unidad': 'PAQ', 'stock_min': 20, 'precio': 8500},
    ]
    
    for prod_data in productos_data:
        categoria = Categoria.objects.get(nombre=prod_data['categoria'])
        producto, created = Producto.objects.get_or_create(
            codigo=prod_data['codigo'],
            defaults={
                'nombre': prod_data['nombre'],
                'categoria': categoria,
                'unidad_medida': prod_data['unidad'],
                'stock_minimo': Decimal(str(prod_data['stock_min'])),
                'precio_unitario': Decimal(str(prod_data['precio'])),
            }
        )
        if created:
            print(f"  ✓ Producto creado: {producto.codigo} - {producto.nombre}")
    
    # 4. Crear algunos proveedores
    proveedores_data = [
        {
            'razon_social': 'Distribuidora Hotelera S.A.',
            'nombre_contacto': 'María González',
            'email': 'ventas@disthotelera.cl',
            'telefono': '+56 2 2345 6789',
            'direccion': 'Av. Providencia 1234, Santiago'
        },
        {
            'razon_social': 'Alimentos Frescos Ltda.',
            'nombre_contacto': 'Carlos Rodriguez',
            'email': 'pedidos@alimentosfrescos.cl',
            'telefono': '+56 2 2876 5432',
            'direccion': 'Los Leones 890, Las Condes'
        },
        {
            'razon_social': 'Bebidas Premium Chile',
            'nombre_contacto': 'Ana Silva',
            'email': 'info@bebidaspremium.cl',
            'telefono': '+56 2 2654 3210',
            'direccion': 'Av. Vitacura 2500, Vitacura'
        },
        {
            'razon_social': 'Textiles Hoteleros del Sur',
            'nombre_contacto': 'Pedro Morales',
            'email': 'ventas@textilesur.cl',
            'telefono': '+56 41 2456 7890',
            'direccion': 'Cochrane 567, Valdivia'
        }
    ]
    
    for prov_data in proveedores_data:
        proveedor, created = Proveedor.objects.get_or_create(
            razon_social=prov_data['razon_social'],
            defaults=prov_data
        )
        if created:
            print(f"  ✓ Proveedor creado: {proveedor.razon_social}")
    
    # 5. Crear stocks iniciales en diferentes áreas
    print("Creando stocks iniciales...")
    bodega = Area.objects.get(nombre='Bodega Principal')
    cocina = Area.objects.get(nombre='Cocina')
    bar = Area.objects.get(nombre='Bar')
    habitaciones_p1 = Area.objects.get(nombre='Habitaciones Piso 1')
    housekeeping = Area.objects.get(nombre='Housekeeping')
    
    # Stocks en bodega (cantidades mayores)
    stocks_bodega = [
        ('AM001', 500), ('AM002', 450), ('AM003', 800), ('AM004', 100),
        ('AF001', 15), ('AF002', 25), ('AS001', 100), ('AS002', 50),
        ('LM001', 20), ('LM002', 30), ('TX001', 100), ('TX002', 50)
    ]
    
    for codigo, cantidad in stocks_bodega:
        producto = Producto.objects.get(codigo=codigo)
        stock, created = Stock.objects.get_or_create(
            producto=producto,
            area=bodega,
            defaults={'cantidad': Decimal(str(cantidad))}
        )
        if created:
            print(f"    ✓ Stock bodega: {producto.nombre} - {cantidad}")
    
    # Stocks en cocina (alimentos)
    stocks_cocina = [
        ('AF001', 3), ('AF002', 8), ('AS001', 15), ('AS002', 10)
    ]
    
    for codigo, cantidad in stocks_cocina:
        producto = Producto.objects.get(codigo=codigo)
        stock, created = Stock.objects.get_or_create(
            producto=producto,
            area=cocina,
            defaults={'cantidad': Decimal(str(cantidad))}
        )
        if created:
            print(f"    ✓ Stock cocina: {producto.nombre} - {cantidad}")
    
    # Stocks en bar (bebidas)
    stocks_bar = [
        ('BB001', 6), ('BB002', 24), ('BN001', 48), ('BN002', 12)
    ]
    
    for codigo, cantidad in stocks_bar:
        producto = Producto.objects.get(codigo=codigo)
        stock, created = Stock.objects.get_or_create(
            producto=producto,
            area=bar,
            defaults={'cantidad': Decimal(str(cantidad))}
        )
        if created:
            print(f"    ✓ Stock bar: {producto.nombre} - {cantidad}")
    
    # Stocks en habitaciones (amenities y bebidas)
    stocks_habitaciones = [
        ('AM001', 20), ('AM002', 20), ('AM003', 30), ('BN001', 12)
    ]
    
    for codigo, cantidad in stocks_habitaciones:
        producto = Producto.objects.get(codigo=codigo)
        stock, created = Stock.objects.get_or_create(
            producto=producto,
            area=habitaciones_p1,
            defaults={'cantidad': Decimal(str(cantidad))}
        )
        if created:
            print(f"    ✓ Stock habitaciones: {producto.nombre} - {cantidad}")
    
    # Stocks en housekeeping (limpieza y textiles)
    stocks_housekeeping = [
        ('LM001', 5), ('LM002', 8), ('TX001', 25), ('TX002', 15)
    ]
    
    for codigo, cantidad in stocks_housekeeping:
        producto = Producto.objects.get(codigo=codigo)
        stock, created = Stock.objects.get_or_create(
            producto=producto,
            area=housekeeping,
            defaults={'cantidad': Decimal(str(cantidad))}
        )
        if created:
            print(f"    ✓ Stock housekeeping: {producto.nombre} - {cantidad}")
    
    print("\n✅ Datos iniciales creados exitosamente!")
    print("\nResumen:")
    print(f"  - Categorías: {Categoria.objects.count()}")
    print(f"  - Áreas: {Area.objects.count()}")
    print(f"  - Productos: {Producto.objects.count()}")
    print(f"  - Proveedores: {Proveedor.objects.count()}")
    print(f"  - Registros de Stock: {Stock.objects.count()}")


if __name__ == '__main__':
    crear_datos_iniciales()
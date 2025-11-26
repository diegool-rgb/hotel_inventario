from django.db import migrations
from decimal import Decimal
from datetime import date, timedelta


def crear_datos_demo(apps, schema_editor):
    Categoria = apps.get_model('inventario', 'Categoria')
    Area = apps.get_model('inventario', 'Area')
    Producto = apps.get_model('inventario', 'Producto')
    Stock = apps.get_model('inventario', 'Stock')
    Proveedor = apps.get_model('inventario', 'Proveedor')
    EntradaStock = apps.get_model('inventario', 'EntradaStock')
    DetalleEntradaStock = apps.get_model('inventario', 'DetalleEntradaStock')
    Movimiento = apps.get_model('inventario', 'Movimiento')
    User = apps.get_model('auth', 'User')

    # Usuario admin (asumimos que ya existe un usuario admin por defecto)
    usuario = User.objects.filter(is_superuser=True).first()
    if not usuario:
        return

    # Asegurar algunas categorias basicas (por si falla 0004)
    cat_names = ['Amenities', 'Bebidas', 'Alimentos', 'Limpieza', 'Mantenimiento', 'Papeleria']
    categorias = {}
    for nombre in cat_names:
        cat, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={'activo': True})
        categorias[nombre] = cat

    # Areas base
    areas_def = [
        ('Bodega Central', 'BODEGA', 'Bodega principal para todo el hotel'),
        ('Cocina Principal', 'COCINA', 'Cocina para restaurante'),
        ('Piso 1 Habitaciones', 'HABITACION', 'Frigobar y amenities piso 1'),
        ('Bar Lobby', 'BAR', 'Bar principal del lobby'),
        ('Lavanderia', 'LIMPIEZA', 'Area de limpieza y lavanderia'),
        ('Recepcion', 'RECEPCION', 'Recepcion y backoffice'),
    ]
    areas = {}
    for nombre, tipo, descripcion in areas_def:
        area, _ = Area.objects.get_or_create(
            nombre=nombre,
            defaults={'tipo': tipo, 'descripcion': descripcion, 'activo': True},
        )
        areas[nombre] = area

    # Proveedor demo
    proveedor, _ = Proveedor.objects.get_or_create(
        rut='99.999.999-9',
        defaults={
            'nombre': 'Proveedor Demo Hotel',
            'telefono': '+56 9 1111 1111',
            'email': 'demo@proveedor.cl',
            'direccion': 'Calle Falsa 123, Ciudad',
            'contacto': 'Soporte Demo',
            'activo': True,
        },
    )

    # Productos demo con distintos comportamientos de stock
    productos_def = [
        # codigo, nombre, categoria, unidad, stock_min, precio, escenario
        ('AME-001', 'Amenity Shampoo 30ml', 'Amenities', 'ML', Decimal('10.00'), Decimal('300'), 'alto'),
        ('AME-002', 'Jabon de manos 20g', 'Amenities', 'GR', Decimal('15.00'), Decimal('150'), 'bajo'),
        ('BEB-001', 'Agua mineral 500ml', 'Bebidas', 'ML', Decimal('24.00'), Decimal('800'), 'agotado'),
        ('BEB-002', 'Cerveza 330ml', 'Bebidas', 'ML', Decimal('24.00'), Decimal('1500'), 'alto'),
        ('ALI-001', 'Pan de molde 1kg', 'Alimentos', 'KG', Decimal('2.00'), Decimal('2000'), 'bajo'),
        ('LIM-001', 'Detergente liquido 5L', 'Limpieza', 'LT', Decimal('1.00'), Decimal('5000'), 'alto'),
        ('OFI-001', 'Resma hoja carta', 'Papeleria', 'PAQ', Decimal('3.00'), Decimal('4000'), 'alto'),
    ]

    productos = {}
    for codigo, nombre, cat_nombre, unidad, stock_min, precio, escenario in productos_def:
        categoria = categorias.get(cat_nombre)
        if not categoria:
            continue
        prod, _ = Producto.objects.get_or_create(
            codigo=codigo,
            defaults={
                'nombre': nombre,
                'categoria': categoria,
                'unidad_medida': unidad,
                'stock_minimo': stock_min,
                'precio_unitario': precio,
                'descripcion': '',
                'activo': True,
            },
        )
        productos[codigo] = (prod, escenario)

    # Crear algunas entradas y movimientos para generar stock variado
    hoy = date.today()

    for idx, (codigo, (producto, escenario)) in enumerate(productos.items(), start=1):
        area_bodega = areas.get('Bodega Central')
        if not area_bodega:
            continue

        # Crear una entrada principal
        numero = f'FAC-DEMO-{idx:03d}'
        entrada = EntradaStock.objects.create(
            numero_entrada=numero,
            tipo='COMPRA',
            proveedor=proveedor,
            fecha_compra=hoy - timedelta(days=7),
            total_compra=producto.precio_unitario * Decimal('50'),
            observaciones='Entrada demo automatica',
            registrado_por=usuario,
        )

        cantidad_inicial = Decimal('50')
        DetalleEntradaStock.objects.create(
            entrada=entrada,
            producto=producto,
            area_destino=area_bodega,
            cantidad=cantidad_inicial,
            precio_unitario=producto.precio_unitario,
        )

        stock, _ = Stock.objects.get_or_create(
            producto=producto,
            area=area_bodega,
            defaults={'cantidad': Decimal('0')},
        )
        stock.cantidad = cantidad_inicial
        stock.save()

        Movimiento.objects.create(
            producto=producto,
            area_origen=None,
            area_destino=area_bodega,
            tipo='ENTRADA',
            motivo='COMPRA',
            cantidad=cantidad_inicial,
            precio_unitario=producto.precio_unitario,
            usuario=usuario,
            observaciones=f'Entrada demo {numero}',
            entrada=entrada,
        )

        # Ahora generar salidas para dejar distintos niveles de stock
        if escenario == 'alto':
            consumo = Decimal('10')
        elif escenario == 'bajo':
            consumo = Decimal('45')
        elif escenario == 'agotado':
            consumo = Decimal('50')
        else:
            consumo = Decimal('20')

        if consumo > 0:
            stock.cantidad -= consumo
            if stock.cantidad < 0:
                stock.cantidad = Decimal('0')
            stock.save()

            Movimiento.objects.create(
                producto=producto,
                area_origen=area_bodega,
                area_destino=None,
                tipo='SALIDA',
                motivo='CONSUMO',
                cantidad=consumo,
                precio_unitario=producto.precio_unitario,
                usuario=usuario,
                observaciones='Consumo demo para ajustar stock',
            )


def eliminar_datos_demo(apps, schema_editor):
    Producto = apps.get_model('inventario', 'Producto')
    Stock = apps.get_model('inventario', 'Stock')
    Movimiento = apps.get_model('inventario', 'Movimiento')
    EntradaStock = apps.get_model('inventario', 'EntradaStock')
    DetalleEntradaStock = apps.get_model('inventario', 'DetalleEntradaStock')

    codigos = ['AME-001', 'AME-002', 'BEB-001', 'BEB-002', 'ALI-001', 'LIM-001', 'OFI-001']

    productos = list(Producto.objects.filter(codigo__in=codigos))
    Movimiento.objects.filter(producto__in=productos).delete()
    DetalleEntradaStock.objects.filter(producto__in=productos).delete()
    EntradaStock.objects.filter(detalles__producto__in=productos).delete()
    Stock.objects.filter(producto__in=productos).delete()
    Producto.objects.filter(id__in=[p.id for p in productos]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_seed_default_data'),
    ]

    operations = [
        migrations.RunPython(crear_datos_demo, eliminar_datos_demo),
    ]

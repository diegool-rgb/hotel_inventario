from django.db import migrations


def crear_categorias(apps, schema_editor):
    Categoria = apps.get_model('inventario', 'Categoria')
    categorias = [
        ('Amenities', 'Articulos de cortesia y amenidades para habitaciones.'),
        ('Bebidas', 'Bebidas alcoholicas y no alcoholicas disponibles en el hotel.'),
        ('Alimentos', 'Productos alimenticios para cocina, restaurante o room service.'),
        ('Limpieza', 'Insumos y productos utilizados en aseo y sanitizacion.'),
        ('Mantenimiento', 'Herramientas y materiales para mantenimiento general.'),
        ('Papeleria', 'Utiles de oficina, informes y material impreso.'),
    ]

    for nombre, descripcion in categorias:
        Categoria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': descripcion, 'activo': True},
        )


def eliminar_categorias(apps, schema_editor):
    Categoria = apps.get_model('inventario', 'Categoria')
    nombres = [
        'Amenities',
        'Bebidas',
        'Alimentos',
        'Limpieza',
        'Mantenimiento',
        'Papeleria',
    ]
    Categoria.objects.filter(nombre__in=nombres).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_movimiento_detalle_entrada_movimiento_entrada_and_more'),
    ]

    operations = [
        migrations.RunPython(crear_categorias, eliminar_categorias),
    ]

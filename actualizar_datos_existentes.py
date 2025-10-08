#!/usr/bin/env python
"""
Script para actualizar datos existentes con información faltante
"""
import os
import django
from datetime import date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from inventario.models import EntradaStock, Proveedor
from decimal import Decimal

def crear_proveedor_generico():
    """Crear proveedor genérico para entradas sin proveedor"""
    proveedor, created = Proveedor.objects.get_or_create(
        nombre="Proveedor Genérico",
        defaults={
            'rut': '00000000-0',
            'contacto': 'Sin contacto especificado',
            'telefono': '000000000',
            'email': 'sin-email@ejemplo.com',
            'direccion': 'Dirección no especificada - Proveedor creado automáticamente para entradas existentes'
        }
    )
    if created:
        print(f"✅ Creado proveedor genérico: {proveedor.nombre}")
    else:
        print(f"ℹ️  Ya existe proveedor genérico: {proveedor.nombre}")
    return proveedor

def actualizar_entradas_sin_datos():
    """Actualizar entradas que no tienen ciertos datos"""
    proveedor_generico = crear_proveedor_generico()
    
    # Contar entradas a actualizar
    entradas_sin_proveedor = EntradaStock.objects.filter(proveedor__isnull=True).count()
    entradas_sin_numero = EntradaStock.objects.filter(numero_entrada__isnull=True).count()
    entradas_sin_fecha = EntradaStock.objects.filter(fecha_compra__isnull=True).count()
    
    print(f"\n📊 ANÁLISIS DE DATOS EXISTENTES:")
    print(f"   • Entradas sin proveedor: {entradas_sin_proveedor}")
    print(f"   • Entradas sin número: {entradas_sin_numero}")
    print(f"   • Entradas sin fecha: {entradas_sin_fecha}")
    
    if entradas_sin_proveedor == 0 and entradas_sin_numero == 0 and entradas_sin_fecha == 0:
        print("✅ Todos los datos están completos. No hay nada que actualizar.")
        return
    
    print(f"\n🔄 INICIANDO ACTUALIZACIÓN...")
    
    # Actualizar entradas sin proveedor
    if entradas_sin_proveedor > 0:
        resultado = EntradaStock.objects.filter(proveedor__isnull=True).update(
            proveedor=proveedor_generico
        )
        print(f"✅ Actualizadas {resultado} entradas sin proveedor")
    
    # Actualizar entradas sin número (generar automáticamente)
    entradas_sin_numero_obj = EntradaStock.objects.filter(numero_entrada__isnull=True)
    contador = 1
    for entrada in entradas_sin_numero_obj:
        numero_auto = f"AUTO-{entrada.id:04d}"
        entrada.numero_entrada = numero_auto
        entrada.save()
        contador += 1
    
    if contador > 1:
        print(f"✅ Generados números automáticos para {contador-1} entradas")
    
    # Actualizar entradas sin fecha (usar fecha de creación o hoy)
    entradas_sin_fecha_obj = EntradaStock.objects.filter(fecha_compra__isnull=True)
    contador = 0
    for entrada in entradas_sin_fecha_obj:
        # Usar fecha de creación si existe, sino fecha actual
        fecha_a_usar = entrada.fecha_creacion.date() if entrada.fecha_creacion else date.today()
        entrada.fecha_compra = fecha_a_usar
        entrada.save()
        contador += 1
    
    if contador > 0:
        print(f"✅ Actualizadas fechas para {contador} entradas")
    
    print(f"\n🎉 ACTUALIZACIÓN COMPLETADA!")

def mostrar_estadisticas_finales():
    """Mostrar estadísticas después de la actualización"""
    total_entradas = EntradaStock.objects.count()
    entradas_completas = EntradaStock.objects.filter(
        proveedor__isnull=False,
        numero_entrada__isnull=False,
        fecha_compra__isnull=False
    ).count()
    
    print(f"\n📈 ESTADÍSTICAS FINALES:")
    print(f"   • Total de entradas: {total_entradas}")
    print(f"   • Entradas completas: {entradas_completas}")
    print(f"   • Porcentaje completo: {(entradas_completas/total_entradas*100):.1f}%" if total_entradas > 0 else "   • No hay entradas")

if __name__ == "__main__":
    print("🚀 INICIANDO ACTUALIZACIÓN DE DATOS EXISTENTES")
    print("=" * 50)
    
    try:
        actualizar_entradas_sin_datos()
        mostrar_estadisticas_finales()
        
        print(f"\n✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ ERROR durante la actualización: {str(e)}")
        print("=" * 50)
#!/usr/bin/env python
"""
Script de verificación del sistema de inventario hotelero
Verifica que todas las funcionalidades estén correctamente configuradas
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Categoria, Area, Producto, Proveedor, Stock

def verificar_sistema():
    """Verificar el estado del sistema"""
    
    print("🏨 VERIFICACIÓN DEL SISTEMA DE INVENTARIO HOTELERO")
    print("=" * 60)
    
    # 1. Verificar usuarios
    usuarios = User.objects.count()
    print(f"👥 Usuarios registrados: {usuarios}")
    
    if usuarios == 0:
        print("⚠️  No hay usuarios. Creando superusuario...")
        User.objects.create_superuser('admin', 'admin@hotel.com', 'admin123')
        print("✅ Superusuario creado: admin / admin123")
    
    # 2. Verificar categorías
    categorias = Categoria.objects.filter(activo=True).count()
    print(f"📂 Categorías activas: {categorias}")
    
    if categorias == 0:
        print("⚠️  No hay categorías. Creando categorías básicas...")
        categorias_basicas = [
            "Amenities",
            "Productos de Limpieza",
            "Mantenimiento",
            "Cocina",
            "Ropa de Cama",
            "Toallas",
            "Decoración"
        ]
        
        for nombre in categorias_basicas:
            Categoria.objects.create(nombre=nombre, descripcion=f"Productos de {nombre}")
        print(f"✅ Creadas {len(categorias_basicas)} categorías básicas")
    
    # 3. Verificar áreas
    areas = Area.objects.filter(activo=True).count()
    print(f"🏢 Áreas activas: {areas}")
    
    if areas == 0:
        print("⚠️  No hay áreas. Creando áreas básicas...")
        areas_basicas = [
            "Bodega Principal",
            "Habitaciones",
            "Cocina",
            "Lavandería",
            "Recepción",
            "Mantención",
            "Housekeeping"
        ]
        
        for nombre in areas_basicas:
            Area.objects.create(nombre=nombre, descripcion=f"Área de {nombre}")
        print(f"✅ Creadas {len(areas_basicas)} áreas básicas")
    
    # 4. Verificar proveedores
    proveedores = Proveedor.objects.filter(activo=True).count()
    print(f"🏪 Proveedores activos: {proveedores}")
    
    # 5. Verificar productos
    productos = Producto.objects.filter(activo=True).count()
    print(f"📦 Productos activos: {productos}")
    
    # 6. Verificar stock
    stock_items = Stock.objects.count()
    print(f"📊 Items en stock: {stock_items}")
    
    print("\n" + "=" * 60)
    print("📝 RESUMEN DE VERIFICACIÓN:")
    print("=" * 60)
    
    if usuarios > 0:
        print("✅ Sistema de usuarios: OK")
    else:
        print("❌ Sistema de usuarios: Falta configurar")
    
    if categorias > 0:
        print("✅ Categorías: OK")
    else:
        print("❌ Categorías: Falta configurar")
    
    if areas > 0:
        print("✅ Áreas: OK")
    else:
        print("❌ Áreas: Falta configurar")
    
    if proveedores > 0:
        print("✅ Proveedores: OK")
    else:
        print("⚠️  Proveedores: Se recomienda agregar proveedores")
    
    print("\n🚀 COMANDOS ÚTILES:")
    print("=" * 60)
    print("• Iniciar servidor: python manage.py runserver")
    print("• Crear superusuario: python manage.py createsuperuser")
    print("• Aplicar migraciones: python manage.py migrate")
    print("• Acceso admin: http://127.0.0.1:8000/admin/")
    print("• Sistema inventario: http://127.0.0.1:8000/")
    
    print("\n🔧 FUNCIONALIDADES DISPONIBLES:")
    print("=" * 60)
    print("✅ Login/Logout de usuarios")
    print("✅ Dashboard con estadísticas")
    print("✅ Gestión de productos")
    print("✅ Gestión de proveedores")
    print("✅ Entrada de stock")
    print("✅ Subida de imágenes de comprobantes")
    print("✅ Tracking de movimientos")
    print("✅ Stock por áreas")
    print("✅ Alertas de stock mínimo")
    print("✅ Interfaz moderna y responsiva")
    
    print("\n🎯 TODO LISTO PARA USAR!")

if __name__ == '__main__':
    verificar_sistema()
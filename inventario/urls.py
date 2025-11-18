from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    # Página principal (redirige según autenticación)
    path('', views.home, name='home'),
    
    # Dashboard principal (requiere login)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestión de productos
    path('productos/', views.lista_productos, name='productos'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/nuevo/', views.agregar_producto, name='agregar_producto'),
    path('productos/<int:producto_id>/stock/', views.agregar_stock, name='agregar_stock'),
    
    # Gestión de proveedores
    path('proveedores/nuevo/', views.agregar_proveedor, name='agregar_proveedor'),
    
    # Entradas de stock
    path('ingresar-factura/', views.ingresar_factura, name='ingresar_factura'),
    path('entrada-stock-completa/', views.entrada_stock, name='entrada_stock_completa'),
    path('entrada-stock/', views.entrada_stock_simple, name='entrada_stock'),
    path('ajax/agregar-stock/', views.agregar_stock_ajax, name='agregar_stock_ajax'),
    path('api/proveedores-sugeridos/', views.proveedores_sugeridos, name='proveedores_sugeridos'),
    
    # Alertas de stock
    path('alertas/', views.alertas_stock, name='alertas'),

    # Trazabilidad
    path('trazabilidad/', views.trazabilidad, name='trazabilidad'),
    
    # Ayuda
    path('ayuda/', views.ayuda, name='ayuda'),
    
    # APIs
    path('api/stats/', views.api_stats, name='api_stats'),
    path('api/entities/', views.api_entities, name='api_entities'),
    path('api/entities/create/', views.api_create_entity, name='api_create_entity'),
    path('api/entities/delete/', views.api_delete_entity, name='api_delete_entity'),
]
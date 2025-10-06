from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('productos/', views.lista_productos, name='productos'),
    path('productos/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('alertas/', views.alertas_stock, name='alertas'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
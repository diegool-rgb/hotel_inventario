from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from decimal import Decimal
from .models import Producto, Stock, Movimiento, AlertaStock, Area, Categoria


def home(request):
    """Vista de inicio - página principal"""
    if request.user.is_authenticated:
        return dashboard(request)
    
    # Estadísticas públicas básicas
    total_productos = Producto.objects.filter(activo=True).count()
    total_areas = Area.objects.filter(activo=True).count()
    
    context = {
        'total_productos': total_productos,
        'total_areas': total_areas,
    }
    
    return render(request, 'inventario/home.html', context)


@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    # Estadísticas generales
    total_productos = Producto.objects.filter(activo=True).count()
    total_areas = Area.objects.filter(activo=True).count()
    total_categorias = Categoria.objects.filter(activo=True).count()
    
    # Alertas de stock bajo
    alertas_activas = AlertaStock.objects.filter(estado='ACTIVA').count()
    
    # Productos con stock bajo
    productos_stock_bajo = []
    for producto in Producto.objects.filter(activo=True)[:10]:
        if producto.tiene_stock_bajo():
            productos_stock_bajo.append({
                'producto': producto,
                'stock_actual': producto.stock_total(),
                'stock_minimo': producto.stock_minimo,
                'porcentaje': (producto.stock_total() / producto.stock_minimo * 100) if producto.stock_minimo > 0 else 0
            })
    
    # Últimos movimientos
    ultimos_movimientos = Movimiento.objects.select_related(
        'producto', 'area_origen', 'area_destino', 'usuario'
    ).order_by('-fecha')[:8]
    
    # Stock por área
    stock_por_area = []
    for area in Area.objects.filter(activo=True):
        total_productos_area = area.stocks.count()
        valor_stock = area.stocks.aggregate(
            total=Sum('cantidad')
        )['total'] or Decimal('0')
        
        stock_por_area.append({
            'area': area,
            'total_productos': total_productos_area,
            'valor_stock': valor_stock,
        })
    
    # Top categorías por cantidad de productos
    top_categorias = Categoria.objects.filter(activo=True).annotate(
        total_productos=Count('productos')
    ).order_by('-total_productos')[:5]
    
    context = {
        'total_productos': total_productos,
        'total_areas': total_areas,
        'total_categorias': total_categorias,
        'alertas_activas': alertas_activas,
        'productos_stock_bajo': productos_stock_bajo,
        'ultimos_movimientos': ultimos_movimientos,
        'stock_por_area': stock_por_area,
        'top_categorias': top_categorias,
    }
    
    return render(request, 'inventario/dashboard.html', context)


@login_required
def lista_productos(request):
    """Vista para listar productos"""
    productos = Producto.objects.select_related('categoria').filter(activo=True)
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    busqueda = request.GET.get('q')
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(codigo__icontains=busqueda)
        )
    
    # Paginación básica
    productos = productos.order_by('categoria__nombre', 'nombre')
    
    categorias = Categoria.objects.filter(activo=True)
    
    context = {
        'productos': productos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
        'busqueda': busqueda,
    }
    
    return render(request, 'inventario/productos.html', context)


@login_required
def detalle_producto(request, producto_id):
    """Vista de detalle de un producto"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    stocks = Stock.objects.select_related('area').filter(producto=producto)
    movimientos = Movimiento.objects.select_related(
        'area_origen', 'area_destino', 'usuario'
    ).filter(producto=producto).order_by('-fecha')[:20]
    
    context = {
        'producto': producto,
        'stocks': stocks,
        'movimientos': movimientos,
        'stock_total': producto.stock_total(),
        'tiene_stock_bajo': producto.tiene_stock_bajo(),
    }
    
    return render(request, 'inventario/detalle_producto.html', context)


@login_required
def alertas_stock(request):
    """Vista para mostrar alertas de stock"""
    alertas = AlertaStock.objects.select_related(
        'producto', 'area'
    ).filter(estado='ACTIVA').order_by('-fecha_creacion')
    
    context = {
        'alertas': alertas,
    }
    
    return render(request, 'inventario/alertas.html', context)


@login_required
def api_stats(request):
    """API para estadísticas del dashboard"""
    # Datos para gráficos
    stock_por_categoria = []
    for categoria in Categoria.objects.filter(activo=True):
        total_stock = Stock.objects.filter(
            producto__categoria=categoria
        ).aggregate(total=Sum('cantidad'))['total'] or 0
        
        stock_por_categoria.append({
            'categoria': categoria.nombre,
            'total': float(total_stock)
        })
    
    movimientos_recientes = []
    for movimiento in Movimiento.objects.order_by('-fecha')[:7]:
        movimientos_recientes.append({
            'fecha': movimiento.fecha.strftime('%Y-%m-%d'),
            'cantidad': float(movimiento.cantidad),
            'tipo': movimiento.tipo
        })
    
    return JsonResponse({
        'stock_por_categoria': stock_por_categoria,
        'movimientos_recientes': movimientos_recientes
    })

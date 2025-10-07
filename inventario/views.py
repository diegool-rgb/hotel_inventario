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

    # Alertas de stock bajo activas
    productos_stock_bajo = []
    for alerta in AlertaStock.objects.filter(estado='ACTIVA').select_related('producto', 'area')[:10]:
        porcentaje = int((alerta.stock_actual / alerta.stock_minimo * 100)) if alerta.stock_minimo > 0 else 0
        critico = porcentaje < 50
        productos_stock_bajo.append({
            'alerta': alerta,
            'producto': alerta.producto,
            'stock_actual': alerta.stock_actual,
            'stock_minimo': alerta.stock_minimo,
            'porcentaje': porcentaje,
            'area': alerta.area,
            'critico': critico,
        })
    # Ordenar: críticos primero, luego por porcentaje ascendente
    productos_stock_bajo = sorted(productos_stock_bajo, key=lambda x: (0 if x['critico'] else 1, x['porcentaje']))

    # Últimos movimientos
    ultimos_movimientos = Movimiento.objects.select_related(
        'producto', 'area_origen', 'area_destino', 'usuario'
    ).order_by('-fecha')[:8]

    # Stock por área
    stock_por_area = []
    areas = Area.objects.filter(activo=True)
    for area in areas:
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
        'areas': areas,
    }

    return render(request, 'inventario/dashboard.html', context)


@login_required
def lista_productos(request):
    """Vista para listar productos"""
    productos = Producto.objects.select_related('categoria').filter(activo=True)

    # Filtros
    area_param = request.GET.get('area')
    area_seleccionada = None
    if area_param:
        try:
            area_id = int(area_param)
            productos = productos.filter(stocks__area_id=area_id).distinct()
            area_seleccionada = area_id
        except ValueError:
            # Assume it's area name
            productos = productos.filter(stocks__area__nombre=area_param).distinct()
            # Find the area to set selected
            try:
                area_obj = Area.objects.get(nombre=area_param, activo=True)
                area_seleccionada = area_obj.id
            except Area.DoesNotExist:
                pass

    busqueda = request.GET.get('q')
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda)
        )

    # Paginación básica
    productos = productos.order_by('categoria__nombre', 'nombre')

    areas = Area.objects.filter(activo=True)

    context = {
        'productos': productos,
        'areas': areas,
        'area_seleccionada': area_seleccionada,
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
    alertas_list = []
    for alerta in AlertaStock.objects.select_related('producto', 'area').filter(estado='ACTIVA'):
        porcentaje = (alerta.stock_actual / alerta.stock_minimo * 100) if alerta.stock_minimo > 0 else 0
        critico = porcentaje < 50
        alertas_list.append({
            'alerta': alerta,
            'porcentaje': porcentaje,
            'critico': critico,
        })
    # Ordenar: críticos primero, luego por fecha descendente
    alertas_list = sorted(alertas_list, key=lambda x: (0 if x['critico'] else 1, x['alerta'].fecha_creacion), reverse=True)

    context = {
        'alertas': alertas_list,
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

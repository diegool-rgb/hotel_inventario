from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.utils.http import urlencode
from decimal import Decimal
from datetime import date
from .models import Producto, Stock, Movimiento, AlertaStock, Area, Categoria, Proveedor, EntradaStock, DetalleEntradaStock
from .forms import AgregarProductoForm, EntradaStockForm, DetalleEntradaFormSet, ProveedorForm


def home(request):
    """Vista de inicio - página principal"""
    if request.user.is_authenticated:
        # Si está autenticado, redirigir al dashboard
        from django.shortcuts import redirect
        return redirect('inventario:dashboard')
    else:
        # Si no está autenticado, redirigir al login
        from django.shortcuts import redirect
        return redirect('usuarios:login')


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
    """Vista para listar productos con filtros avanzados"""
    from django.db.models import Sum, Prefetch, F
    
    # Query base con optimizaciones
    productos = Producto.objects.select_related('categoria').prefetch_related(
        Prefetch('stocks', queryset=Stock.objects.select_related('area'))
    ).filter(activo=True)
    
    # Agregar stock total y áreas con stock
    productos = productos.annotate(
        stock_total=Sum('stocks__cantidad'),
    )

    # FILTROS
    
    # 1. Filtro por búsqueda (nombre o código)
    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    # 2. Filtro por categoría
    categoria_param = request.GET.get('categoria')
    categoria_seleccionada = None
    if categoria_param:
        try:
            categoria_id = int(categoria_param)
            productos = productos.filter(categoria_id=categoria_id)
            categoria_seleccionada = categoria_id
        except ValueError:
            pass

    # 3. Filtro por área
    area_param = request.GET.get('area')
    area_seleccionada = None
    if area_param:
        try:
            area_id = int(area_param)
            productos = productos.filter(stocks__area_id=area_id).distinct()
            area_seleccionada = area_id
        except ValueError:
            pass

    # 4. Filtro por estado de stock
    stock_filtro = request.GET.get('stock')
    if stock_filtro:
        if stock_filtro == 'agotado':
            productos = productos.filter(stock_total__lte=0)
        elif stock_filtro == 'bajo':
            productos = productos.filter(stock_total__lte=F('stock_minimo'), stock_total__gt=0)
        elif stock_filtro == 'disponible':
            productos = productos.filter(stock_total__gt=0)

    # ORDENAMIENTO
    orden = request.GET.get('orden', 'categoria__nombre')
    orden_valido = [
        'nombre', '-nombre', 'categoria__nombre', 'codigo', 
        '-fecha_creacion', 'stock_total', '-stock_total'
    ]
    
    if orden in orden_valido:
        productos = productos.order_by(orden, 'nombre')
    else:
        productos = productos.order_by('categoria__nombre', 'nombre')

    # Paginación
    from django.core.paginator import Paginator
    
    paginator = Paginator(productos, 12)  # 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Agregar información de áreas con stock para cada producto
    productos_con_areas = []
    for producto in page_obj:
        areas_con_stock = producto.stocks.filter(cantidad__gt=0).values('area__nombre', 'cantidad')
        producto.areas_con_stock = areas_con_stock
        productos_con_areas.append(producto)

    # Datos para el template
    areas = Area.objects.filter(activo=True).order_by('nombre')
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')

    context = {
        'productos': productos_con_areas,
        'page_obj': page_obj,
        'areas': areas,
        'categorias': categorias,
        'area_seleccionada': area_seleccionada,
        'categoria_seleccionada': categoria_seleccionada,
        'busqueda': busqueda,
        'stock_filtro': stock_filtro,
        'orden_actual': orden,
        'total_productos': paginator.count,
    }

    return render(request, 'inventario/productos_con_guia.html', context)


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


def ayuda(request):
    """Vista de ayuda del sistema"""
    return render(request, 'inventario/ayuda.html')


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


@login_required
def agregar_producto(request):
    """Vista para agregar un nuevo producto con stock inicial"""
    if request.method == 'POST':
        form = AgregarProductoForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Crear el producto
                    producto = form.save()
                    
                    # Crear stock inicial si se proporcionó
                    area_inicial = form.cleaned_data.get('area_inicial')
                    cantidad_inicial = form.cleaned_data.get('cantidad_inicial')
                    
                    if area_inicial and cantidad_inicial and cantidad_inicial > 0:
                        # Crear entrada de stock inicial
                        numero_entrada = form.cleaned_data.get('numero_factura') or f'INICIAL-{producto.codigo}'
                        
                        entrada = EntradaStock.objects.create(
                            numero_entrada=numero_entrada,
                            tipo='COMPRA',
                            proveedor=form.cleaned_data.get('proveedor'),
                            fecha_compra=form.cleaned_data.get('fecha_compra') or date.today(),
                            total_compra=cantidad_inicial * (producto.precio_unitario or 0),
                            comprobante=form.cleaned_data.get('comprobante'),
                            observaciones=f'Stock inicial para producto {producto.nombre}',
                            registrado_por=request.user
                        )
                        
                        # Crear detalle de entrada
                        DetalleEntradaStock.objects.create(
                            entrada=entrada,
                            producto=producto,
                            cantidad=cantidad_inicial,
                            precio_unitario=producto.precio_unitario,
                            area_destino=area_inicial
                        )
                        
                        # Crear stock
                        Stock.objects.create(
                            producto=producto,
                            area=area_inicial,
                            cantidad=cantidad_inicial
                        )
                        
                        # Crear movimiento
                        Movimiento.objects.create(
                            producto=producto,
                            area_destino=area_inicial,
                            tipo='ENTRADA',
                            motivo='INICIAL',
                            cantidad=cantidad_inicial,
                            precio_unitario=producto.precio_unitario,
                            usuario=request.user,
                            observaciones=f'Stock inicial: {entrada.numero_entrada}'
                        )
                        
                        messages.success(request, f'¡Producto "{producto.nombre}" creado exitosamente con {cantidad_inicial} {producto.unidad_medida} en {area_inicial.nombre}!')
                    else:
                        messages.success(request, f'¡Producto "{producto.nombre}" creado exitosamente! Puedes agregar stock usando "Entrada de Stock".')
                    
                    return redirect('inventario:productos')
                    
            except Exception as e:
                messages.error(request, f'Error al crear el producto: {str(e)}')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = AgregarProductoForm()
    
    context = {
        'form': form,
        'categorias': Categoria.objects.filter(activo=True),
        'areas': Area.objects.filter(activo=True),
        'proveedores': Proveedor.objects.filter(activo=True),
    }
    return render(request, 'inventario/agregar_producto.html', context)


@login_required
def agregar_stock(request, producto_id):
    """Vista para agregar stock inicial a un producto recién creado"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        entrada_form = EntradaStockForm(request.POST, request.FILES)
        detalle_formset = DetalleEntradaFormSet(request.POST, prefix='detalles')
        
        if entrada_form.is_valid() and detalle_formset.is_valid():
            try:
                with transaction.atomic():
                    # Crear la entrada
                    entrada = entrada_form.save(commit=False)
                    entrada.registrado_por = request.user
                    entrada.save()
                    
                    # Procesar los detalles
                    for detalle_form in detalle_formset:
                        if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE'):
                            detalle = detalle_form.save(commit=False)
                            detalle.entrada = entrada
                            detalle.save()
                            
                            # Actualizar o crear stock
                            stock, created = Stock.objects.get_or_create(
                                producto=detalle.producto,
                                area=detalle.area_destino,
                                defaults={'cantidad': detalle.cantidad}
                            )
                            if not created:
                                stock.cantidad += detalle.cantidad
                                stock.save()
                            
                            # Crear movimiento
                            Movimiento.objects.create(
                                producto=detalle.producto,
                                area=detalle.area_destino,
                                tipo='ENTRADA',
                                cantidad=detalle.cantidad,
                                usuario=request.user,
                                observaciones=f'Entrada: {entrada.numero_entrada}'
                            )
                    
                    messages.success(request, f'¡Stock agregado exitosamente! Entrada registrada: {entrada.numero_entrada}')
                    return redirect('inventario:productos')
                    
            except Exception as e:
                messages.error(request, f'Error al procesar la entrada: {str(e)}')
    else:
        # Inicializar formularios
        entrada_form = EntradaStockForm()
        detalle_formset = DetalleEntradaFormSet(prefix='detalles')
        
        # Pre-llenar el primer detalle con el producto actual
        if detalle_formset.forms:
            detalle_formset.forms[0].initial = {'producto': producto}
    
    context = {
        'producto': producto,
        'entrada_form': entrada_form,
        'detalle_formset': detalle_formset,
        'proveedores': Proveedor.objects.filter(activo=True),
        'areas': Area.objects.filter(activo=True),
        'productos': Producto.objects.filter(activo=True),
    }
    return render(request, 'inventario/agregar_stock.html', context)


@login_required
def agregar_proveedor(request):
    """Vista para agregar un nuevo proveedor"""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save()
            messages.success(request, f'¡Proveedor "{proveedor.nombre}" agregado exitosamente!')
            return redirect('inventario:agregar_stock', producto_id=request.GET.get('producto_id', 1))
    else:
        form = ProveedorForm()
    
    context = {
        'form': form,
        'producto_id': request.GET.get('producto_id'),
    }
    return render(request, 'inventario/agregar_proveedor.html', context)


@login_required
def entrada_stock(request):
    """Vista mejorada para registrar nueva entrada de stock con búsqueda de productos"""
    from datetime import date
    
    # Obtener parámetros de búsqueda
    busqueda = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    area_id = request.GET.get('area', '')
    
    # Generar próximo número de entrada automáticamente
    ultima_entrada_num = EntradaStock.objects.all().order_by('-id').first()
    if ultima_entrada_num:
        try:
            # Extraer número de la última entrada si tiene formato numérico
            ultimo_num = int(ultima_entrada_num.numero_entrada.split('-')[-1])
            proximo_numero = f"ENT-{ultimo_num + 1:04d}"
        except:
            # Si no se puede extraer número, usar timestamp
            from datetime import datetime
            proximo_numero = f"ENT-{datetime.now().strftime('%m%d%H%M')}"
    else:
        proximo_numero = "ENT-0001"
    
    # Construir queryset con filtros
    productos_query = Producto.objects.filter(activo=True).select_related('categoria')
    
    # Anotar con stock total
    productos_query = productos_query.annotate(
        stock_total=Sum('stocks__cantidad')
    )
    
    # Filtrar por búsqueda
    if busqueda:
        productos_query = productos_query.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    # Filtrar por categoría
    if categoria_id:
        productos_query = productos_query.filter(categoria_id=categoria_id)
    
    # Filtrar por área (productos que tengan stock en esa área)
    if area_id:
        productos_query = productos_query.filter(stocks__area_id=area_id).distinct()
    
    # Obtener áreas con stock para cada producto y datos inteligentes
    productos = []
    for producto in productos_query[:50]:  # Limitar a 50 para mejor rendimiento
        areas_con_stock = Stock.objects.filter(
            producto=producto,
            cantidad__gt=0
        ).select_related('area')
        
        # Obtener datos de la última entrada de este producto para auto-completar
        ultima_entrada = DetalleEntradaStock.objects.filter(
            producto=producto
        ).select_related('entrada', 'entrada__proveedor', 'area_destino').order_by('-entrada__fecha_compra').first()
        
        # Agregar datos inteligentes al producto
        if ultima_entrada:
            producto.ultimo_proveedor = ultima_entrada.entrada.proveedor
            producto.ultima_area_destino = ultima_entrada.area_destino
            producto.ultimo_precio_unitario = ultima_entrada.precio_unitario
            producto.ultima_cantidad = ultima_entrada.cantidad
        else:
            producto.ultimo_proveedor = None
            producto.ultima_area_destino = None
            producto.ultimo_precio_unitario = None
            producto.ultima_cantidad = None
        
        producto.areas_con_stock = areas_con_stock
        productos.append(producto)
    
    # Manejo del POST para crear entrada de stock
    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        numero_entrada = request.POST.get('numero_entrada')
        fecha_compra = request.POST.get('fecha_compra')
        proveedor_id = request.POST.get('proveedor')
        total_compra = request.POST.get('total_compra')
        area_destino_id = request.POST.get('area_destino')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        observaciones = request.POST.get('observaciones', '')
        comprobante = request.FILES.get('comprobante')
        
        if not all([producto_id, numero_entrada, fecha_compra, area_destino_id, cantidad]):
            messages.error(request, 'Por favor completa todos los campos obligatorios.')
        else:
            try:
                with transaction.atomic():
                    # Crear la entrada
                    entrada = EntradaStock.objects.create(
                        numero_entrada=numero_entrada,
                        fecha_compra=fecha_compra,
                        proveedor_id=proveedor_id if proveedor_id else None,
                        total_compra=Decimal(total_compra) if total_compra else None,
                        observaciones=observaciones,
                        comprobante=comprobante,
                        registrado_por=request.user
                    )
                    
                    # Obtener producto y área
                    producto = Producto.objects.get(id=producto_id)
                    area = Area.objects.get(id=area_destino_id)
                    cantidad_decimal = Decimal(cantidad)
                    precio_decimal = Decimal(precio_unitario) if precio_unitario else None
                    
                    # Crear detalle de entrada
                    detalle = DetalleEntradaStock.objects.create(
                        entrada=entrada,
                        producto=producto,
                        cantidad=cantidad_decimal,
                        precio_unitario=precio_decimal,
                        area_destino=area
                    )
                    
                    # Actualizar o crear stock
                    stock, created = Stock.objects.get_or_create(
                        producto=producto,
                        area=area,
                        defaults={'cantidad': cantidad_decimal}
                    )
                    if not created:
                        stock.cantidad += cantidad_decimal
                        stock.save()
                    
                    # Crear movimiento
                    Movimiento.objects.create(
                        producto=producto,
                        area=area,
                        tipo='ENTRADA',
                        cantidad=cantidad_decimal,
                        usuario=request.user,
                        observaciones=f'Entrada: {entrada.numero_entrada}'
                    )
                    
                    messages.success(request, f'¡Stock agregado exitosamente! Entrada registrada: {entrada.numero_entrada}')
                    # Redirigir manteniendo filtros
                    url_params = {}
                    if busqueda:
                        url_params['q'] = busqueda
                    if categoria_id:
                        url_params['categoria'] = categoria_id
                    if area_id:
                        url_params['area'] = area_id
                    
                    if url_params:
                        return redirect(f"{reverse('inventario:entrada_stock')}?{urlencode(url_params)}")
                    else:
                        return redirect('inventario:entrada_stock')
                        
            except Exception as e:
                messages.error(request, f'Error al procesar la entrada: {str(e)}')
    
    context = {
        'productos': productos,
        'total_productos': len(productos),
        'busqueda': busqueda,
        'categoria_seleccionada': int(categoria_id) if categoria_id else None,
        'area_seleccionada': int(area_id) if area_id else None,
        'categorias': Categoria.objects.filter(activo=True),
        'areas': Area.objects.filter(activo=True),
        'proveedores': Proveedor.objects.filter(activo=True),
        'fecha_hoy': date.today().isoformat(),
        'proximo_numero_entrada': proximo_numero,
    }
    return render(request, 'inventario/entrada_stock.html', context)

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Categoria, Area, Producto, Stock, Movimiento, AlertaStock,
    Proveedor, EntradaStock, DetalleEntradaStock
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'total_productos', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']
    
    def total_productos(self, obj):
        return obj.productos.count()
    total_productos.short_description = 'Total Productos'


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'activo', 'total_stocks']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre', 'descripcion']
    ordering = ['tipo', 'nombre']
    
    def total_stocks(self, obj):
        return obj.stocks.count()
    total_stocks.short_description = 'Productos en Stock'


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'categoria', 'unidad_medida', 'stock_minimo', 'stock_total_display', 'activo']
    list_filter = ['categoria', 'unidad_medida', 'activo', 'fecha_creacion']
    search_fields = ['codigo', 'nombre', 'descripcion']
    ordering = ['categoria__nombre', 'nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'nombre', 'categoria', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('unidad_medida', 'stock_minimo', 'precio_unitario', 'activo')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_total_display(self, obj):
        stock = obj.stock_total()
        if obj.tiene_stock_bajo():
            return format_html('<span style="color: red; font-weight: bold;">{} {}</span>', 
                             stock, obj.get_unidad_medida_display().lower())
        return f"{stock} {obj.get_unidad_medida_display().lower()}"
    stock_total_display.short_description = 'Stock Total'


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['producto', 'area', 'cantidad', 'unidad_medida', 'fecha_actualizacion']
    list_filter = ['area', 'producto__categoria', 'fecha_actualizacion']
    search_fields = ['producto__codigo', 'producto__nombre', 'area__nombre']
    ordering = ['area__nombre', 'producto__nombre']
    
    def unidad_medida(self, obj):
        return obj.producto.get_unidad_medida_display()
    unidad_medida.short_description = 'Unidad'


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'producto', 'tipo', 'motivo', 'cantidad', 'area_origen', 'area_destino', 'usuario']
    list_filter = ['tipo', 'motivo', 'fecha', 'area_origen', 'area_destino']
    search_fields = ['producto__codigo', 'producto__nombre', 'observaciones']
    ordering = ['-fecha']
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Movimiento', {
            'fields': ('producto', 'tipo', 'motivo', 'cantidad')
        }),
        ('Áreas', {
            'fields': ('area_origen', 'area_destino')
        }),
        ('Detalles Financieros', {
            'fields': ('precio_unitario',)
        }),
        ('Información Adicional', {
            'fields': ('observaciones', 'usuario', 'fecha')
        }),
    )


@admin.register(AlertaStock)
class AlertaStockAdmin(admin.ModelAdmin):
    list_display = ['producto', 'area', 'stock_actual', 'stock_minimo', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'area', 'fecha_creacion']
    search_fields = ['producto__codigo', 'producto__nombre']
    ordering = ['-fecha_creacion']
    readonly_fields = ['fecha_creacion']
    
    actions = ['marcar_como_resuelta', 'marcar_como_ignorada']
    
    def marcar_como_resuelta(self, request, queryset):
        queryset.update(estado='RESUELTA', resuelto_por=request.user)
        self.message_user(request, f'{queryset.count()} alertas marcadas como resueltas.')
    marcar_como_resuelta.short_description = 'Marcar como resuelta'
    
    def marcar_como_ignorada(self, request, queryset):
        queryset.update(estado='IGNORADA', resuelto_por=request.user)
        self.message_user(request, f'{queryset.count()} alertas marcadas como ignoradas.')
    marcar_como_ignorada.short_description = 'Marcar como ignorada'


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rut', 'telefono', 'email', 'contacto', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'rut', 'contacto', 'email']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion']


class DetalleEntradaInline(admin.TabularInline):
    model = DetalleEntradaStock
    extra = 1
    fields = ['producto', 'area_destino', 'cantidad', 'precio_unitario']


@admin.register(EntradaStock)
class EntradaStockAdmin(admin.ModelAdmin):
    list_display = ['numero_entrada', 'tipo', 'proveedor', 'fecha_compra', 'total_compra', 'registrado_por', 'fecha_entrada']
    list_filter = ['tipo', 'fecha_compra', 'fecha_entrada', 'proveedor']
    search_fields = ['numero_entrada', 'proveedor__nombre', 'observaciones']
    ordering = ['-fecha_entrada']
    readonly_fields = ['fecha_entrada', 'registrado_por']
    inlines = [DetalleEntradaInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es nuevo
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(DetalleEntradaStock)
class DetalleEntradaStockAdmin(admin.ModelAdmin):
    list_display = ['entrada', 'producto', 'area_destino', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['entrada__fecha_entrada', 'area_destino', 'producto__categoria']
    search_fields = ['producto__nombre', 'producto__codigo', 'entrada__numero_entrada']
    ordering = ['-entrada__fecha_entrada']

from django.contrib import admin
from django.utils.html import format_html
from .models import Proveedor, Pedido, DetallePedido, RecepcionPedido, DetalleRecepcion


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'nombre_contacto', 'email', 'telefono', 'activo', 'total_pedidos']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['razon_social', 'nombre_contacto', 'email']
    ordering = ['razon_social']
    
    def total_pedidos(self, obj):
        return obj.pedidos.count()
    total_pedidos.short_description = 'Total Pedidos'


class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ['subtotal']
    
    def subtotal(self, obj):
        if obj.pk:
            return f"${obj.subtotal():,.2f}"
        return "-"
    subtotal.short_description = 'Subtotal'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero_pedido', 'proveedor', 'fecha_pedido', 'fecha_entrega_estimada', 
                   'estado', 'total_items', 'total_pedido_display', 'creado_por']
    list_filter = ['estado', 'fecha_pedido', 'proveedor']
    search_fields = ['numero_pedido', 'proveedor__razon_social', 'observaciones']
    ordering = ['-fecha_pedido']
    readonly_fields = ['numero_pedido', 'fecha_creacion', 'fecha_actualizacion', 'total_pedido_display']
    date_hierarchy = 'fecha_pedido'
    inlines = [DetallePedidoInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('numero_pedido', 'proveedor', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_entrega_estimada', 'fecha_entrega_real')
        }),
        ('Detalles', {
            'fields': ('observaciones', 'total_pedido_display')
        }),
        ('Metadatos', {
            'fields': ('creado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def total_pedido_display(self, obj):
        if obj.pk:
            total = obj.total_pedido()
            return format_html('<strong>${:,.2f}</strong>', total)
        return "-"
    total_pedido_display.short_description = 'Total Pedido'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad_pedida', 'cantidad_recibida', 
                   'precio_unitario', 'subtotal_display', 'esta_completo']
    list_filter = ['pedido__estado', 'producto__categoria']
    search_fields = ['pedido__numero_pedido', 'producto__codigo', 'producto__nombre']
    ordering = ['-pedido__fecha_pedido', 'producto__nombre']
    
    def subtotal_display(self, obj):
        return f"${obj.subtotal():,.2f}"
    subtotal_display.short_description = 'Subtotal'


class DetalleRecepcionInline(admin.TabularInline):
    model = DetalleRecepcion
    extra = 0


@admin.register(RecepcionPedido)
class RecepcionPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'fecha_recepcion', 'recibido_por', 'total_items_recibidos']
    list_filter = ['fecha_recepcion', 'recibido_por']
    search_fields = ['pedido__numero_pedido', 'observaciones']
    ordering = ['-fecha_recepcion']
    readonly_fields = ['fecha_recepcion']
    inlines = [DetalleRecepcionInline]
    
    def total_items_recibidos(self, obj):
        return obj.detalles.count()
    total_items_recibidos.short_description = 'Items Recibidos'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.recibido_por = request.user
        super().save_model(request, obj, form, change)

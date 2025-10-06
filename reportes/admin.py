from django.contrib import admin
from django.utils.html import format_html
from .models import TipoReporte, Reporte, ConfiguracionReporte, LogReporte


@admin.register(TipoReporte)
class TipoReporteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'template_nombre', 'activo', 'total_reportes']
    list_filter = ['activo']
    search_fields = ['nombre', 'descripcion', 'template_nombre']
    ordering = ['nombre']
    
    def total_reportes(self, obj):
        return obj.reportes.count()
    total_reportes.short_description = 'Total Reportes'


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_reporte', 'formato', 'estado', 'generado_por', 
                   'fecha_generacion', 'tamaño_archivo_display']
    list_filter = ['tipo_reporte', 'formato', 'estado', 'fecha_generacion']
    search_fields = ['nombre', 'observaciones', 'generado_por__username']
    ordering = ['-fecha_generacion']
    readonly_fields = ['fecha_generacion', 'tamaño_archivo_display']
    date_hierarchy = 'fecha_generacion'
    
    fieldsets = (
        ('Información del Reporte', {
            'fields': ('tipo_reporte', 'nombre', 'formato', 'estado')
        }),
        ('Filtros de Date', {
            'fields': ('fecha_desde', 'fecha_hasta')
        }),
        ('Filtros de Contenido', {
            'fields': ('categorias', 'areas', 'productos'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('generado_por', 'fecha_generacion', 'archivo_path', 
                      'tamaño_archivo_display', 'observaciones')
        }),
    )
    
    filter_horizontal = ['categorias', 'areas', 'productos']
    
    def tamaño_archivo_display(self, obj):
        if obj.tamaño_archivo:
            if obj.tamaño_archivo < 1024:
                return f"{obj.tamaño_archivo} bytes"
            elif obj.tamaño_archivo < 1024 * 1024:
                return f"{obj.tamaño_archivo / 1024:.1f} KB"
            else:
                return f"{obj.tamaño_archivo / (1024 * 1024):.1f} MB"
        return "N/A"
    tamaño_archivo_display.short_description = 'Tamaño'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.generado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(ConfiguracionReporte)
class ConfiguracionReporteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_reporte', 'frecuencia', 'formato', 'activo', 
                   'proximo_envio', 'ultimo_envio']
    list_filter = ['frecuencia', 'formato', 'activo', 'tipo_reporte']
    search_fields = ['nombre', 'emails_destino']
    ordering = ['nombre']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Configuración Básica', {
            'fields': ('nombre', 'tipo_reporte', 'frecuencia', 'formato', 'activo')
        }),
        ('Destinatarios', {
            'fields': ('emails_destino',)
        }),
        ('Programación', {
            'fields': ('proximo_envio', 'ultimo_envio')
        }),
        ('Filtros por Defecto', {
            'fields': ('categorias_default', 'areas_default'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('creado_por', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['categorias_default', 'areas_default']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(LogReporte)
class LogReporteAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'accion', 'reporte', 'configuracion', 'usuario', 'detalle_corto']
    list_filter = ['accion', 'fecha']
    search_fields = ['detalle', 'reporte__nombre', 'configuracion__nombre']
    ordering = ['-fecha']
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
    
    def detalle_corto(self, obj):
        if obj.detalle:
            return obj.detalle[:50] + ('...' if len(obj.detalle) > 50 else '')
        return "-"
    detalle_corto.short_description = 'Detalle'

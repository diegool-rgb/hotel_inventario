from django.db import models
from django.contrib.auth.models import User
from inventario.models import Categoria, Area, Producto


class TipoReporte(models.Model):
    """Tipos de reportes disponibles en el sistema"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    template_nombre = models.CharField(max_length=100, help_text="Nombre del template para generar el reporte")
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Tipo de Reporte"
        verbose_name_plural = "Tipos de Reporte"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Reporte(models.Model):
    """Reportes generados por el sistema"""
    ESTADOS = [
        ('GENERADO', 'Generado'),
        ('ENVIADO', 'Enviado'),
        ('ERROR', 'Error en Generación'),
    ]
    
    FORMATOS = [
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
        ('CSV', 'CSV'),
    ]
    
    tipo_reporte = models.ForeignKey(TipoReporte, on_delete=models.CASCADE, related_name='reportes')
    nombre = models.CharField(max_length=200)
    formato = models.CharField(max_length=10, choices=FORMATOS, default='PDF')
    fecha_desde = models.DateField(null=True, blank=True)
    fecha_hasta = models.DateField(null=True, blank=True)
    
    # Filtros opcionales
    categorias = models.ManyToManyField(Categoria, blank=True, help_text="Filtrar por categorías")
    areas = models.ManyToManyField(Area, blank=True, help_text="Filtrar por áreas")
    productos = models.ManyToManyField(Producto, blank=True, help_text="Filtrar por productos específicos")
    
    # Metadatos del reporte
    estado = models.CharField(max_length=15, choices=ESTADOS, default='GENERADO')
    generado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reportes_generados')
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    archivo_path = models.CharField(max_length=500, blank=True, null=True)
    tamaño_archivo = models.IntegerField(null=True, blank=True, help_text="Tamaño en bytes")
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Reporte"
        verbose_name_plural = "Reportes"
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha_generacion.strftime('%d/%m/%Y %H:%M')}"


class ConfiguracionReporte(models.Model):
    """Configuraciones para reportes automáticos"""
    FRECUENCIAS = [
        ('DIARIO', 'Diario'),
        ('SEMANAL', 'Semanal'),
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo_reporte = models.ForeignKey(TipoReporte, on_delete=models.CASCADE, related_name='configuraciones')
    frecuencia = models.CharField(max_length=15, choices=FRECUENCIAS)
    formato = models.CharField(max_length=10, choices=Reporte.FORMATOS, default='PDF')
    
    # Destinatarios
    emails_destino = models.TextField(help_text="Emails separados por comas")
    
    # Configuración de envío
    activo = models.BooleanField(default=True)
    proximo_envio = models.DateTimeField(null=True, blank=True)
    ultimo_envio = models.DateTimeField(null=True, blank=True)
    
    # Filtros por defecto
    categorias_default = models.ManyToManyField(Categoria, blank=True)
    areas_default = models.ManyToManyField(Area, blank=True)
    
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='configuraciones_reporte')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Configuración de Reporte"
        verbose_name_plural = "Configuraciones de Reporte"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_frecuencia_display()}"


class LogReporte(models.Model):
    """Log de generación y envío de reportes"""
    ACCIONES = [
        ('GENERADO', 'Reporte Generado'),
        ('ENVIADO', 'Reporte Enviado'),
        ('ERROR_GENERACION', 'Error en Generación'),
        ('ERROR_ENVIO', 'Error en Envío'),
    ]
    
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    configuracion = models.ForeignKey(ConfiguracionReporte, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    fecha = models.DateTimeField(auto_now_add=True)
    detalle = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Log de Reporte"
        verbose_name_plural = "Logs de Reporte"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.get_accion_display()} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"

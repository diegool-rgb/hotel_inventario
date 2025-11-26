from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from inventario.models import Producto


class Proveedor(models.Model):
    """Proveedores del hotel"""
    razon_social = models.CharField(max_length=200)
    nombre_contacto = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['razon_social']
    
    def __str__(self):
        return self.razon_social


class Pedido(models.Model):
    """Pedidos a proveedores"""
    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADO', 'Enviado'),
        ('CONFIRMADO', 'Confirmado'),
        ('PARCIAL', 'Recibido Parcial'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    numero_pedido = models.CharField(max_length=50, unique=True, blank=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_entrega_estimada = models.DateField(null=True, blank=True)
    fecha_entrega_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='BORRADOR')
    observaciones = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='pedidos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_pedido']
    
    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.proveedor.razon_social}"
    
    def save(self, *args, **kwargs):
        if not self.numero_pedido:
            # Generar número de pedido automático
            fecha_referencia = self.fecha_pedido or timezone.now()
            year = fecha_referencia.year
            count = Pedido.objects.filter(fecha_pedido__year=year).count() + 1
            self.numero_pedido = f"PED-{year}-{count:04d}"
        super().save(*args, **kwargs)
    
    def total_pedido(self):
        """Calcula el total del pedido"""
        return self.detalles.aggregate(
            total=models.Sum(
                models.F('cantidad') * models.F('precio_unitario'),
                output_field=models.DecimalField(max_digits=12, decimal_places=2)
            )
        )['total'] or Decimal('0')
    
    def total_items(self):
        """Cuenta el total de items en el pedido"""
        return self.detalles.count()


class DetallePedido(models.Model):
    """Detalle de productos en un pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_pedido')
    cantidad_pedida = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    cantidad_recibida = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))],
        default=Decimal('0')
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))]
    )
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedido"
        unique_together = ['pedido', 'producto']
        ordering = ['producto__nombre']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad_pedida} {self.producto.get_unidad_medida_display()}"
    
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.cantidad_pedida * self.precio_unitario
    
    def cantidad_pendiente(self):
        """Calcula la cantidad pendiente de recibir"""
        return self.cantidad_pedida - self.cantidad_recibida
    
    def esta_completo(self):
        """Verifica si el item está completamente recibido"""
        return self.cantidad_recibida >= self.cantidad_pedida


class RecepcionPedido(models.Model):
    """Registro de recepción de pedidos"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='recepciones')
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    recibido_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='recepciones_pedido')
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Recepción de Pedido"
        verbose_name_plural = "Recepciones de Pedido"
        ordering = ['-fecha_recepcion']
    
    def __str__(self):
        return f"Recepción {self.pedido.numero_pedido} - {self.fecha_recepcion.strftime('%d/%m/%Y %H:%M')}"


class DetalleRecepcion(models.Model):
    """Detalle de productos recibidos en una recepción"""
    recepcion = models.ForeignKey(RecepcionPedido, on_delete=models.CASCADE, related_name='detalles')
    detalle_pedido = models.ForeignKey(DetallePedido, on_delete=models.CASCADE, related_name='recepciones')
    cantidad_recibida = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Detalle de Recepción"
        verbose_name_plural = "Detalles de Recepción"
        ordering = ['detalle_pedido__producto__nombre']
    
    def __str__(self):
        return f"{self.detalle_pedido.producto.nombre} - {self.cantidad_recibida}"

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Categoria(models.Model):
    """Categorías de productos (Amenities, Bebidas, Alimentos, Limpieza, etc.)"""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Area(models.Model):
    """Áreas del hotel donde se almacenan productos (Bodega, Cocina, Habitaciones, etc.)"""
    TIPOS_AREA = [
        ('BODEGA', 'Bodega Principal'),
        ('COCINA', 'Cocina'),
        ('HABITACION', 'Habitaciones/Frigo Bar'),
        ('BAR', 'Bar'),
        ('LIMPIEZA', 'Área de Limpieza'),
        ('RECEPCION', 'Recepción'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS_AREA)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
        ordering = ['tipo', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Producto(models.Model):
    """Productos del inventario"""
    UNIDADES_MEDIDA = [
        ('UN', 'Unidad'),
        ('KG', 'Kilogramo'),
        ('LT', 'Litro'),
        ('ML', 'Mililitro'),
        ('GR', 'Gramo'),
        ('PAQ', 'Paquete'),
        ('CAJ', 'Caja'),
        ('BOT', 'Botella'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, help_text="Código único del producto")
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    unidad_medida = models.CharField(max_length=3, choices=UNIDADES_MEDIDA)
    stock_minimo = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))],
        help_text="Stock mínimo antes de generar alerta"
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))],
        null=True,
        blank=True,
        help_text="Precio unitario de referencia"
    )
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['categoria__nombre', 'nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def stock_total(self):
        """Calcula el stock total sumando todas las áreas"""
        return self.stocks.aggregate(
            total=models.Sum('cantidad')
        )['total'] or Decimal('0')
    
    def tiene_stock_bajo(self):
        """Verifica si el producto tiene stock bajo"""
        return self.stock_total() <= self.stock_minimo


class Stock(models.Model):
    """Stock de productos por área"""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='stocks')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='stocks')
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))],
        default=Decimal('0')
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"
        unique_together = ['producto', 'area']
        ordering = ['area__nombre', 'producto__nombre']
    
    def __str__(self):
        return f"{self.producto.nombre} en {self.area.nombre}: {self.cantidad} {self.producto.get_unidad_medida_display()}"


class Movimiento(models.Model):
    """Registro de movimientos de inventario"""
    TIPOS_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste de Inventario'),
        ('TRANSFERENCIA', 'Transferencia entre Áreas'),
    ]
    
    MOTIVOS = [
        ('COMPRA', 'Compra'),
        ('DEVOLUCION', 'Devolución'),
        ('CONSUMO', 'Consumo'),
        ('VENTA', 'Venta'),
        ('PERDIDA', 'Pérdida/Merma'),
        ('AJUSTE_INVENTARIO', 'Ajuste de Inventario'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('INICIAL', 'Stock Inicial'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    area_origen = models.ForeignKey(
        Area, 
        on_delete=models.CASCADE, 
        related_name='movimientos_origen',
        null=True, 
        blank=True,
        help_text="Área de origen (para transferencias y salidas)"
    )
    area_destino = models.ForeignKey(
        Area, 
        on_delete=models.CASCADE, 
        related_name='movimientos_destino',
        null=True, 
        blank=True,
        help_text="Área de destino (para transferencias y entradas)"
    )
    tipo = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0'))],
        null=True,
        blank=True
    )
    observaciones = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='movimientos_inventario')
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.producto.nombre} - {self.cantidad} {self.producto.get_unidad_medida_display()}"
    
    def valor_total(self):
        """Calcula el valor total del movimiento"""
        if self.precio_unitario:
            return self.cantidad * self.precio_unitario
        return None


class AlertaStock(models.Model):
    """Alertas de stock bajo"""
    ESTADOS = [
        ('ACTIVA', 'Activa'),
        ('RESUELTA', 'Resuelta'),
        ('IGNORADA', 'Ignorada'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='alertas')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='alertas', null=True, blank=True)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ACTIVA')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    resuelto_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alertas_resueltas'
    )
    observaciones = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Alerta de Stock"
        verbose_name_plural = "Alertas de Stock"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        area_text = f" en {self.area.nombre}" if self.area else ""
        return f"Alerta: {self.producto.nombre}{area_text} - Stock: {self.stock_actual}"


class Proveedor(models.Model):
    """Proveedores de productos"""
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=15, unique=True, help_text="RUT del proveedor")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True, help_text="Nombre del contacto principal")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class EntradaStock(models.Model):
    """Registro de entradas de stock (compras)"""
    TIPOS_ENTRADA = [
        ('COMPRA', 'Compra'),
        ('DONACION', 'Donación'),
        ('AJUSTE', 'Ajuste de Inventario'),
        ('DEVOLUCION', 'Devolución'),
    ]
    
    numero_entrada = models.CharField(max_length=50, unique=True, help_text="Número de factura o documento")
    tipo = models.CharField(max_length=20, choices=TIPOS_ENTRADA, default='COMPRA')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT, related_name='entradas', null=True, blank=True)
    fecha_compra = models.DateField(help_text="Fecha de la compra/factura")
    fecha_entrada = models.DateTimeField(auto_now_add=True, help_text="Fecha de registro en el sistema")
    comprobante = models.ImageField(
        upload_to='comprobantes/', 
        null=True, 
        blank=True, 
        help_text="Foto de la boleta/factura"
    )
    total_compra = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Total de la compra (opcional)"
    )
    observaciones = models.TextField(blank=True, null=True)
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='entradas_registradas')
    
    class Meta:
        verbose_name = "Entrada de Stock"
        verbose_name_plural = "Entradas de Stock"
        ordering = ['-fecha_entrada']
    
    def __str__(self):
        return f"Entrada {self.numero_entrada} - {self.fecha_compra}"


class DetalleEntradaStock(models.Model):
    """Detalle de productos en cada entrada de stock"""
    entrada = models.ForeignKey(EntradaStock, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    area_destino = models.ForeignKey(Area, on_delete=models.PROTECT, help_text="Área donde se almacena")
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Precio unitario de compra"
    )
    
    class Meta:
        verbose_name = "Detalle de Entrada"
        verbose_name_plural = "Detalles de Entrada"
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} {self.producto.unidad_medida}"
    
    def subtotal(self):
        """Calcula el subtotal del producto"""
        if self.precio_unitario:
            return self.cantidad * self.precio_unitario
        return None

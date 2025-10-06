from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    """Perfil extendido para usuarios del sistema"""
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('JEFE_AYB', 'Jefe de Alimentos y Bebidas'),
        ('HOUSEKEEPING', 'Housekeeping'),
        ('GARZON', 'Garzón/Restaurante'),
        ('BODEGUERO', 'Bodeguero'),
        ('GERENCIA', 'Gerencia'),
    ]
    
    AREAS_ACCESO = [
        ('TODAS', 'Todas las Áreas'),
        ('BODEGA', 'Solo Bodega'),
        ('COCINA', 'Solo Cocina'),
        ('HABITACIONES', 'Solo Habitaciones'),
        ('BAR', 'Solo Bar'),
        ('LIMPIEZA', 'Solo Limpieza'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES)
    area_acceso = models.CharField(max_length=20, choices=AREAS_ACCESO, default='TODAS')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Permisos específicos
    puede_crear_pedidos = models.BooleanField(default=False)
    puede_recibir_pedidos = models.BooleanField(default=False)
    puede_ajustar_inventario = models.BooleanField(default=False)
    puede_ver_reportes = models.BooleanField(default=False)
    puede_administrar_productos = models.BooleanField(default=False)
    puede_administrar_usuarios = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        ordering = ['user__username']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_rol_display()}"
    
    def nombre_completo(self):
        return self.user.get_full_name() or self.user.username
    
    def es_administrador(self):
        return self.rol == 'ADMIN'
    
    def puede_acceder_area(self, area_tipo):
        """Verifica si el usuario puede acceder a un área específica"""
        if self.area_acceso == 'TODAS' or self.es_administrador():
            return True
        return self.area_acceso == area_tipo


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario"""
    if created:
        PerfilUsuario.objects.create(user=instance, rol='GARZON')


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """Guarda el perfil cuando se actualiza el usuario"""
    if hasattr(instance, 'perfil'):
        instance.perfil.save()


class SesionUsuario(models.Model):
    """Registro de sesiones de usuarios para auditoría"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sesiones')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Sesión de Usuario"
        verbose_name_plural = "Sesiones de Usuario"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"
    
    def duracion(self):
        """Calcula la duración de la sesión"""
        if self.fecha_fin:
            return self.fecha_fin - self.fecha_inicio
        return None

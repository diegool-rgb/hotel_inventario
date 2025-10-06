from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import PerfilUsuario, SesionUsuario


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil'


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilUsuarioInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'area_acceso', 'activo', 'fecha_creacion']
    list_filter = ['rol', 'area_acceso', 'activo', 'fecha_creacion']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['user__username']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información del Perfil', {
            'fields': ('rol', 'area_acceso', 'telefono', 'activo')
        }),
        ('Permisos Específicos', {
            'fields': ('puede_crear_pedidos', 'puede_recibir_pedidos', 'puede_ajustar_inventario',
                      'puede_ver_reportes', 'puede_administrar_productos', 'puede_administrar_usuarios'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(SesionUsuario)
class SesionUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha_inicio', 'fecha_fin', 'duracion_display', 'ip_address', 'activa']
    list_filter = ['activa', 'fecha_inicio', 'fecha_fin']
    search_fields = ['usuario__username', 'ip_address']
    ordering = ['-fecha_inicio']
    readonly_fields = ['fecha_inicio', 'fecha_fin', 'duracion_display']
    
    def duracion_display(self, obj):
        duracion = obj.duracion()
        if duracion:
            total_seconds = int(duracion.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "En curso" if obj.activa else "N/A"
    duracion_display.short_description = 'Duración'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usuario')

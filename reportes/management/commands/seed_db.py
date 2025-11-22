from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
from django.utils import timezone

from inventario.models import (
    Categoria, Area, Producto, Stock, Movimiento, Proveedor as InvProveedor,
    EntradaStock, DetalleEntradaStock, AlertaStock
)
from pedidos.models import (
    Proveedor as PedProveedor, Pedido, DetallePedido, RecepcionPedido, DetalleRecepcion
)
from reportes.models import TipoReporte, Reporte, ConfiguracionReporte, LogReporte
from usuarios.models import PerfilUsuario


class Command(BaseCommand):
    help = 'Siembra datos de ejemplo en la base de datos (usuarios, productos, proveedores, pedidos, reportes)'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando siembra de datos de ejemplo...')
        with transaction.atomic():
            self._create_users()
            self._create_categorias_areas_proveedores()
            self._create_productos_y_stocks()
            self._create_entradas_movimientos()
            self._create_pedidos_y_recepciones()
            self._create_reportes()

        self.stdout.write(self.style.SUCCESS('Siembra completada.'))

    def _create_users(self):
        # Usuario admin (superuser)
        admin, created = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@hotel.local',
            'is_staff': True,
            'is_superuser': True,
        })
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write('- Usuario `admin` creado')
        else:
            # Asegurarse de que la contraseña sea la requerida (sobrescribe)
            admin.set_password('admin123')
            admin.is_staff = True
            admin.is_superuser = True
            admin.email = 'admin@hotel.local'
            admin.save()
            self.stdout.write('- Usuario `admin` actualizado')

        # Usuario hotelpresidente (usuario normal con rol GERENCIA)
        hp, created = User.objects.get_or_create(username='hotelpresidente', defaults={
            'email': 'presidente@hotel.local',
            'is_staff': False,
            'is_superuser': False,
        })
        if created:
            hp.set_password('1234')
            hp.save()
            self.stdout.write('- Usuario `hotelpresidente` creado')
        else:
            hp.set_password('1234')
            hp.email = 'presidente@hotel.local'
            hp.save()
            self.stdout.write('- Usuario `hotelpresidente` actualizado')

        # Crear perfiles y asignar permisos apropiados
        perfil_admin, _ = PerfilUsuario.objects.get_or_create(user=admin)
        perfil_admin.rol = 'ADMIN'
        perfil_admin.puede_administrar_usuarios = True
        perfil_admin.puede_administrar_productos = True
        perfil_admin.puede_ver_reportes = True
        perfil_admin.puede_ajustar_inventario = True
        perfil_admin.area_acceso = 'TODAS'
        perfil_admin.save()

        perfil_hp, _ = PerfilUsuario.objects.get_or_create(user=hp)
        perfil_hp.rol = 'GERENCIA'
        perfil_hp.puede_ver_reportes = True
        perfil_hp.area_acceso = 'TODAS'
        perfil_hp.save()

    def _create_categorias_areas_proveedores(self):
        categorias = [
            ('ALIM', 'Alimentos y Despensa'),
            ('BEB', 'Bebidas'),
            ('LIM', 'Limpieza y Aseo'),
            ('AMEN', 'Amenities y Aseo Personal'),
            ('FRUT', 'Frutas y Verduras'),
        ]
        for code, name in categorias:
            Categoria.objects.get_or_create(nombre=name, defaults={'descripcion': f'Categoría {name}'})

        areas = [
            ('Bodega Principal', 'BODEGA'),
            ('Cocina Central', 'COCINA'),
            ('Bar Principal', 'BAR'),
            ('Habitaciones', 'HABITACION'),
            ('Limpieza', 'LIMPIEZA'),
            ('Recepción', 'RECEPCION'),
        ]
        for nombre, tipo in areas:
            Area.objects.get_or_create(nombre=nombre, tipo=tipo)

        # Proveedores para inventario y pedidos
        proveedores_inv = [
            ('Distribuciones Chile Ltda', '76.123.456-7', 'contacto@distchile.cl'),
            ('Bebidas del Sur S.A.', '78.987.654-3', 'ventas@bebidassur.cl'),
            ('LimpioPro', '80.555.444-2', 'info@limpiopro.cl'),
        ]
        for nombre, rut, email in proveedores_inv:
            InvProveedor.objects.get_or_create(rut=rut, defaults={'nombre': nombre, 'email': email})

        proveedores_ped = [
            ('Proveedor Hotelero Ltda', 'proveedor1@hotel.cl', '+56911111111'),
            ('Mayorista Gastronomico', 'mayorista@gastro.cl', '+56922222222'),
        ]
        for razon, email, telefono in proveedores_ped:
            PedProveedor.objects.get_or_create(razon_social=razon, defaults={'email': email, 'telefono': telefono})

    def _create_productos_y_stocks(self):
        # Obtener categorías y áreas
        categorias = {c.nombre: c for c in Categoria.objects.all()}
        areas = {a.tipo: a for a in Area.objects.all()}

        productos = [
            ('ALIM-001', 'Arroz 1kg', 'Alimentos y Despensa', 'KG', '10', '1500.00'),
            ('ALIM-002', 'Harina 1kg', 'Alimentos y Despensa', 'KG', '5', '900.00'),
            ('BEB-001', 'Agua 500ml', 'Bebidas', 'BOT', '20', '400.00'),
            ('BEB-002', 'Cerveza 330ml', 'Bebidas', 'BOT', '30', '800.00'),
            ('LIM-001', 'Detergente 5L', 'Limpieza y Aseo', 'LT', '2', '8000.00'),
            ('AMN-001', 'Shampoo Hotel 30ml', 'Amenities y Aseo Personal', 'ML', '50', '120.00'),
            ('FRU-001', 'Manzana', 'Frutas y Verduras', 'KG', '5', '2000.00'),
        ]

        for codigo, nombre, cat_nombre, unidad, stock_min, precio in productos:
            cat = Categoria.objects.filter(nombre=cat_nombre).first() or Categoria.objects.first()
            producto, created = Producto.objects.get_or_create(codigo=codigo, defaults={
                'nombre': nombre,
                'categoria': cat,
                'unidad_medida': unidad,
                'stock_minimo': Decimal(stock_min),
                'precio_unitario': Decimal(precio),
                'descripcion': f'Producto {nombre} de ejemplo',
            })
            if created:
                self.stdout.write(f'- Producto {codigo} creado')
            else:
                # actualizar precios/stock_minimo si hace falta
                producto.precio_unitario = Decimal(precio)
                producto.stock_minimo = Decimal(stock_min)
                producto.save()

            # Crear stocks en varias áreas
            for area in Area.objects.all():
                # dar cantidades diferentes por tipo de área
                if area.tipo == 'BODEGA':
                    cantidad = Decimal('100')
                elif area.tipo == 'COCINA':
                    cantidad = Decimal('30')
                elif area.tipo == 'BAR':
                    cantidad = Decimal('50')
                elif area.tipo == 'HABITACION':
                    cantidad = Decimal('20')
                else:
                    cantidad = Decimal('10')

                stock, _ = Stock.objects.get_or_create(producto=producto, area=area, defaults={'cantidad': cantidad})
                # solo actualizar si es menor que el valor deseado
                if stock.cantidad < cantidad:
                    stock.cantidad = cantidad
                    stock.save()

    def _create_entradas_movimientos(self):
        # Usar el usuario admin como registrado
        admin = User.objects.filter(username='admin').first()
        prov = InvProveedor.objects.first()
        if not prov or not admin:
            return

        # Crear una entrada de stock por proveedor con detalle
        entrada, created = EntradaStock.objects.get_or_create(
            numero_entrada='FAC-0001',
            defaults={
                'tipo': 'COMPRA',
                'proveedor': prov,
                'fecha_compra': timezone.now().date(),
                'total_compra': Decimal('0'),
                'registrado_por': admin,
            }
        )
        if created:
            self.stdout.write('- Entrada de stock FAC-0001 creada')

        total = Decimal('0')
        # Añadir detalles para algunos productos
        for producto in Producto.objects.all()[:5]:
            detalle, dcreated = DetalleEntradaStock.objects.get_or_create(
                entrada=entrada,
                producto=producto,
                area_destino=Area.objects.filter(tipo='BODEGA').first(),
                defaults={'cantidad': Decimal('50'), 'precio_unitario': producto.precio_unitario or Decimal('0')}
            )
            if dcreated:
                Movimiento.objects.create(
                    producto=producto,
                    area_origen=None,
                    area_destino=detalle.area_destino,
                    tipo='ENTRADA',
                    motivo='COMPRA',
                    cantidad=detalle.cantidad,
                    precio_unitario=detalle.precio_unitario,
                    usuario=admin,
                    entrada=entrada,
                    detalle_entrada=detalle,
                )
            total += (detalle.precio_unitario or Decimal('0')) * detalle.cantidad

        entrada.total_compra = total
        entrada.save()

    def _create_pedidos_y_recepciones(self):
        admin = User.objects.filter(username='admin').first()
        proveedor = PedProveedor.objects.first()
        if not admin or not proveedor:
            return

        pedido, created = Pedido.objects.get_or_create(numero_pedido='PED-2025-0001', defaults={
            'proveedor': proveedor,
            'estado': 'ENVIADO',
            'creado_por': admin,
        })
        if created:
            self.stdout.write('- Pedido PED-2025-0001 creado')

        for producto in Producto.objects.all()[:4]:
            DetallePedido.objects.get_or_create(
                pedido=pedido,
                producto=producto,
                defaults={'cantidad_pedida': Decimal('20'), 'precio_unitario': producto.precio_unitario or Decimal('0')}
            )

        # Simular recepción parcial
        recepcion = RecepcionPedido.objects.create(pedido=pedido, recibido_por=admin, observaciones='Recepción de prueba')
        for detalle in pedido.detalles.all():
            cantidad_rec = detalle.cantidad_pedida / 2
            DetalleRecepcion.objects.create(recepcion=recepcion, detalle_pedido=detalle, cantidad_recibida=cantidad_rec)
            # actualizar detalle pedido
            detalle.cantidad_recibida = cantidad_rec
            detalle.save()

    def _create_reportes(self):
        admin = User.objects.filter(username='admin').first()
        if not admin:
            return

        tipos = [
            ('Stock Critico', 'Reporte de productos con stock por debajo del mínimo', 'reportes/stock_critico.html'),
            ('Movimientos', 'Reporte de movimientos de inventario', 'reportes/movimientos.html'),
        ]
        for nombre, descripcion, tpl in tipos:
            TipoReporte.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion, 'template_nombre': tpl})

        tr = TipoReporte.objects.filter(nombre='Stock Critico').first()
        if tr:
            rep, _ = Reporte.objects.get_or_create(nombre='Stock crítico inicial', tipo_reporte=tr, defaults={'generado_por': admin, 'formato': 'CSV'})

        # Configuración de reporte semanal
        cfg, _ = ConfiguracionReporte.objects.get_or_create(nombre='Envio semanal stock', tipo_reporte=tr, defaults={
            'frecuencia': 'SEMANAL', 'formato': 'CSV', 'emails_destino': 'gerencia@hotel.local', 'creado_por': admin
        })

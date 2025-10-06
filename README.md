# Sistema de Inventario Hotelero

Un sistema web moderno para la gestión integral de inventario hotelero, desarrollado con Django y Bootstrap 5.

## 🏨 Características Principales

- **Control en Tiempo Real**: Monitoreo automático de stock por área
- **Alertas Inteligentes**: Prevención de pedidos de emergencia costosos
- **Gestión por Roles**: Accesos específicos para cada responsabilidad del hotel
- **Interfaz Moderna**: Diseño responsive con Bootstrap 5
- **Datos Reales**: Basado en insights de operación hotelera real

## 🎯 Problema Resuelto

**Antes**: *"El sistema actual no existe como tal; solo usamos Excel y mucha confianza"*

**Después**: Sistema digital centralizado que elimina:
- Pedidos de emergencia costosos
- Errores detectados tarde o nunca
- Acceso restringido a una sola persona
- Gastos extra en combustible y tiempo

## Características Principales

### 🏨 **Gestión de Inventario**
- Control de stock por áreas (Bodega, Cocina, Habitaciones, Bar, etc.)
- Categorización de productos (Amenities, Bebidas, Alimentos, Limpieza, Textiles)
- Alertas automáticas de stock bajo
- Historial completo de movimientos
- Ajustes de inventario con trazabilidad

### 📦 **Gestión de Pedidos**
- Pedidos a proveedores con seguimiento de estado
- Recepción parcial y total de mercadería
- Control de precios y costos
- Historial de compras por proveedor

### 👥 **Gestión de Usuarios**
- Roles específicos: Admin, Jefe A&B, Housekeeping, Garzón, Bodeguero
- Permisos granulares por área y funcionalidad
- Auditoría de sesiones y acciones

### 📊 **Reportes y Análisis**
- Reportes de stock por área y categoría
- Reportes de movimientos y consumo
- Exportación a PDF, Excel y CSV
- Configuración de reportes automáticos

## Estructura del Proyecto

```
hotel_inventario/
├── config/                 # Configuración del proyecto Django
├── inventario/             # App principal - gestión de stock
├── pedidos/               # App de pedidos a proveedores
├── reportes/              # App de generación de reportes
├── usuarios/              # App de gestión de usuarios y perfiles
├── static/                # Archivos estáticos (CSS, JS, imágenes)
├── templates/             # Templates HTML
├── media/                 # Archivos subidos por usuarios
├── logs/                  # Logs del sistema
└── data_inicial.py        # Script para cargar datos de prueba
```

## Modelos Principales

### Inventario
- **Categoria**: Clasificación de productos
- **Area**: Áreas del hotel donde se almacenan productos
- **Producto**: Productos del inventario con stock mínimo
- **Stock**: Stock actual por producto y área
- **Movimiento**: Registro de todas las transacciones
- **AlertaStock**: Alertas de stock bajo

### Pedidos
- **Proveedor**: Proveedores del hotel
- **Pedido**: Pedidos realizados a proveedores
- **DetallePedido**: Detalle de productos por pedido
- **RecepcionPedido**: Registro de recepciones
- **DetalleRecepcion**: Detalle de productos recibidos

## Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- Django 5.2
- SQLite (desarrollo) / MySQL (producción)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd hotel_inventario
   ```

📋 **[Ver guía completa de instalación para colaboradores](INSTALACION.md)**

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

6. **Cargar datos iniciales (opcional)**
   ```bash
   python data_inicial.py
   ```

7. **Ejecutar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

8. **Acceder al sistema**
   - Panel de administración: http://localhost:8000/admin/
   - Usuario y contraseña: los configurados en el paso 5

## Datos de Prueba

El script `data_inicial.py` carga:
- 8 categorías de productos
- 7 áreas del hotel
- 16 productos de ejemplo
- 4 proveedores
- 28 registros de stock distribuidos en las áreas

### Productos de Ejemplo Incluidos:
- **Amenities**: Shampoo, Acondicionador, Jabón, Zapatillas
- **Bebidas**: Vinos, Cervezas, Agua, Jugos
- **Alimentos**: Salmón, Verduras, Arroz, Pasta
- **Limpieza**: Detergentes, Desinfectantes
- **Textiles**: Toallas, Sábanas

## Casos de Uso Principales

### 1. **Registro de Consumo**
- Registrar consumo de amenities por habitación
- Descontar stock automáticamente
- Generar alerta si stock queda bajo el mínimo

### 2. **Transferencias entre Áreas**
- Trasladar productos de bodega a cocina
- Transferir amenities a habitaciones
- Mantener trazabilidad completa

### 3. **Gestión de Pedidos**
- Crear pedido cuando stock esté bajo
- Recibir mercadería y actualizar stock
- Controlar precios y costos

### 4. **Reportes para Casa Matriz**
- Generar reportes consolidados
- Exportar en diferentes formatos
- Programar envíos automáticos

## Configuración Adicional

### Variables de Configuración (settings.py)
```python
HOTEL_CONFIG = {
    'NOMBRE_HOTEL': 'Hotel Sistema de Inventario',
    'MONEDA': 'CLP',  # Pesos chilenos
    'FORMATO_FECHA': '%d/%m/%Y',
    'FORMATO_DATETIME': '%d/%m/%Y %H:%M',
    'EMAIL_REPORTES': 'reportes@hotel.com',
    'STOCK_CRITICO_PORCENTAJE': 10,
}
```

### Roles de Usuario Disponibles
- **ADMIN**: Acceso completo al sistema
- **JEFE_AYB**: Jefe de Alimentos y Bebidas
- **HOUSEKEEPING**: Personal de limpieza
- **GARZON**: Personal de restaurante
- **BODEGUERO**: Encargado de bodega
- **GERENCIA**: Gerencia del hotel

## Próximos Pasos

1. **Desarrollo de Vistas Web**: Crear interfaz web para usuarios finales
2. **API REST**: Implementar API para integración con otros sistemas
3. **Reportes Avanzados**: Agregar más tipos de reportes y dashboards
4. **Integración con Proveedores**: Envío automático de pedidos
5. **App Móvil**: Desarrollar aplicación móvil para el personal

## Soporte y Contacto

Para soporte técnico o consultas sobre el sistema, contactar al equipo de desarrollo.

---

**Versión**: 1.0.0  
**Fecha**: Octubre 2024  
**Tecnología**: Django 5.2, Python 3.8+, SQLite/MySQL  
**Licencia**: Uso interno del hotel
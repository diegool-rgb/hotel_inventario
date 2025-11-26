# Hotel Inventario

Sistema Django para gestionar existencias, compras y reportes del hotel.

## Requisitos previos
- Git
- Python 3.11 o superior (con `pip`)
- PostgreSQL 15+ y pgAdmin 4
- Opcional: entorno virtual (recomendado)

## Instalación (paso a paso)
1. **Clona el repositorio**
   ```bash
   git clone https://github.com/diegool-rgb/hotel_inventario.git
   ```
2. **Ingresa al directorio**
   ```bash
   cd hotel_inventario
   ```
3. **Crea un entorno virtual**
   ```bash
   python -m venv .venv
   ```
4. **Activa el entorno**
   - Windows: `.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`
5. **Actualiza `pip`**
   ```bash
   python -m pip install --upgrade pip
   ```
6. **Instala dependencias**
   ```bash
   pip install -r requirements.txt
   ```
7. **Configura la base de datos PostgreSQL** (ver sección siguiente). Ajusta variables en `config/settings.py` o usa variables de entorno si lo prefieres.
8. **Ejecuta migraciones**
   ```bash
   python manage.py migrate
   ```
9. **(Opcional) Crea un superusuario**
   ```bash
   python manage.py createsuperuser
   ```
10. **Inicia el servidor de desarrollo**
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```

## Configuración de PostgreSQL / pgAdmin
1. Abre pgAdmin y conecta al servidor local (`postgres` / contraseña configurada durante la instalación).
2. En el árbol de la izquierda haz clic derecho en **Databases → Create → Database** y crea `Hotel_Inventario` con owner `postgres`.
3. Verifica que el servicio PostgreSQL escuche en `localhost:5432`.
4. Asegúrate de que las credenciales en `config/settings.py` coincidan (por defecto: usuario `postgres`, contraseña `Inacap2025`).
5. Si cambias los valores (host, puerto, usuario, contraseña), actualízalos y reinicia el servidor Django.
6. Vuelve a pgAdmin para revisar que las tablas aparezcan después de correr `python manage.py migrate`.

## Variables sensibles
- `SECRET_KEY` y credenciales de BD están en `config/settings.py` solo para desarrollo. Antes de producción muévelos a variables de entorno o a un `.env`.

## Ejecutar pruebas básicas
```bash
python manage.py test
```

## Contacto
Para soporte del proyecto escribe a Diego Henríquez (mantainer actual) o abre un issue en GitHub.

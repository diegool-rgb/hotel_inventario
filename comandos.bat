@echo off
REM Script de comandos útiles para el Sistema de Inventario Hotelero
REM Uso: comandos.bat [opcion]

if "%1"=="" goto menu
if "%1"=="help" goto menu
if "%1"=="servidor" goto servidor
if "%1"=="admin" goto admin
if "%1"=="datos" goto datos
if "%1"=="hotel" goto hotel
if "%1"=="shell" goto shell
if "%1"=="migraciones" goto migraciones
if "%1"=="backup" goto backup
if "%1"=="logs" goto logs
if "%1"=="git" goto git
goto menu

:menu
echo ========================================
echo  Sistema de Inventario Hotelero
echo ========================================
echo.
echo Comandos disponibles:
echo.
echo  servidor     - Iniciar servidor de desarrollo
echo  admin        - Crear superusuario
echo  datos        - Cargar datos iniciales
echo  hotel        - Poblar con datos reales del hotel
echo  shell        - Abrir shell de Django
echo  migraciones  - Crear y aplicar migraciones
echo  backup       - Crear backup de la base de datos
echo  logs         - Ver logs del sistema
echo  git          - Comandos Git (commit y push)
echo  help         - Mostrar esta ayuda
echo.
echo Uso: comandos.bat [comando]
echo Ejemplo: comandos.bat servidor
echo.
goto end

:servidor
echo Iniciando servidor de desarrollo...
echo Accede a: http://localhost:8000/admin/
echo Presiona Ctrl+C para detener
echo.
C:/Users/diego/Documents/hotel_inventario/.venv/Scripts/python.exe manage.py runserver
goto end

:admin
echo Creando superusuario...
C:/Users/diego/Documents/hotel_inventario/.venv/Scripts/python.exe manage.py createsuperuser
goto end

:datos
echo Cargando datos iniciales...
C:/Users/diego/Documents/hotel_inventario/.venv/Scripts/python.exe data_inicial.py
echo.
echo Datos cargados exitosamente!
echo Puedes acceder al admin con tu superusuario.
goto end

:hotel
echo Poblando sistema con datos reales del hotel...
echo Basado en insights de la entrevista con la administradora...
echo.
C:/Users/diego/Documents/hotel_inventario/.venv/Scripts/python.exe poblar_hotel_real.py
echo.
echo ^[32mDatos del hotel cargados exitosamente!^[0m
echo Areas: Housekeeping, Restaurante, Cocina, Habitaciones
echo Productos: Amenities, Frigobar, Limpieza, Abarrotes
echo Alertas: Simulacion de stock bajo para prevenir emergencias
echo.
goto end

:shell
echo Abriendo shell de Django...
C:/Users/diego/Documents/hotel_inventario/.venv/Scripts/python.exe manage.py shell
goto end

:migraciones
echo Creando migraciones...
C:/Users/diego/Documents/hotel_inventario/.venv/Scripts/python.exe manage.py makemigrations
echo.
echo Aplicando migraciones...
C:/Users/diego/Documents/hotel_inventario/.venv/Scripts/python.exe manage.py migrate
echo.
echo Migraciones completadas!
goto end

:backup
echo Creando backup de la base de datos...
if not exist backups mkdir backups
set fecha=%date:~-4,4%%date:~-10,2%%date:~-7,2%
set hora=%time:~0,2%%time:~3,2%
set hora=%hora: =0%
copy db.sqlite3 "backups\db_backup_%fecha%_%hora%.sqlite3"
echo Backup creado: backups\db_backup_%fecha%_%hora%.sqlite3
goto end

:logs
echo Mostrando logs del sistema...
if exist logs\hotel_inventario.log (
    type logs\hotel_inventario.log | more
) else (
    echo No se encontraron logs. El archivo se creará cuando ejecutes el servidor.
)
goto end

:git
echo ========================================
echo  Comandos Git - Sistema de Inventario
echo ========================================
echo.
set /p mensaje="Ingresa el mensaje del commit: "
echo.
echo Agregando archivos...
git add .
echo.
echo Haciendo commit...
git commit -m "%mensaje%"
echo.
echo Subiendo a GitHub...
git push origin main
echo.
echo ^[32mCódigo subido exitosamente a GitHub!^[0m
goto end

:end
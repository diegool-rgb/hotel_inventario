@echo off
REM Script de instalación automática para el Sistema de Inventario Hotelero
REM Para nuevos colaboradores y usuarios

echo ========================================
echo  Sistema de Inventario Hotelero
echo  Script de Instalacion Automatica
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ^[31m❌ ERROR: Python no está instalado^[0m
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo Asegurate de marcar "Add to PATH" durante la instalacion
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado correctamente

REM Verificar si Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ^[33m⚠️ ADVERTENCIA: Git no está instalado^[0m
    echo Si descargaste el ZIP, puedes continuar
    echo Si quieres colaborar, instala Git desde: https://git-scm.com/downloads
    echo.
)

echo.
echo 🚀 Iniciando instalación automática...
echo.

REM Crear entorno virtual
echo 📦 Creando entorno virtual...
python -m venv .venv
if errorlevel 1 (
    echo ^[31m❌ ERROR: No se pudo crear el entorno virtual^[0m
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔌 Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Actualizar pip
echo 🔄 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ^[31m❌ ERROR: No se pudieron instalar las dependencias^[0m
    pause
    exit /b 1
)

REM Crear migraciones
echo 🗄️ Configurando base de datos...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ^[31m❌ ERROR: Problemas con la base de datos^[0m
    pause
    exit /b 1
)

REM Preguntar si crear superusuario
echo.
set /p crear_admin="¿Quieres crear un usuario administrador? (s/n): "
if /i "%crear_admin%"=="s" (
    echo 👤 Creando usuario administrador...
    python manage.py createsuperuser
)

REM Preguntar qué datos cargar
echo.
echo 📊 ¿Qué datos quieres cargar?
echo 1. Datos básicos de prueba
echo 2. Datos reales del hotel (recomendado)
echo 3. No cargar datos ahora
set /p opcion_datos="Elige una opción (1-3): "

if "%opcion_datos%"=="1" (
    echo 📄 Cargando datos básicos...
    python data_inicial.py
) else if "%opcion_datos%"=="2" (
    echo 🏨 Cargando datos reales del hotel...
    python poblar_hotel_real.py
) else (
    echo ⏭️ Saltando carga de datos
)

echo.
echo ^[32m🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!^[0m
echo.
echo 📋 Próximos pasos:
echo.
echo 1. Para iniciar el servidor:
echo    ^[36mcomandos.bat servidor^[0m
echo    o
echo    ^[36mpython manage.py runserver^[0m
echo.
echo 2. Acceder al sistema:
echo    ^[36mhttp://127.0.0.1:8000/^[0m
echo.
echo 3. Panel de administración:
echo    ^[36mhttp://127.0.0.1:8000/admin/^[0m
echo.
echo 4. Ver comandos disponibles:
echo    ^[36mcomandos.bat help^[0m
echo.
echo 📞 Soporte: dg1604719@gmail.com
echo 📚 Documentación: https://github.com/diegool-rgb/hotel_inventario
echo.

set /p iniciar="¿Quieres iniciar el servidor ahora? (s/n): "
if /i "%iniciar%"=="s" (
    echo.
    echo 🚀 Iniciando servidor de desarrollo...
    python manage.py runserver
) else (
    echo.
    echo ✅ Instalación completa. ¡El sistema está listo para usar!
    pause
)
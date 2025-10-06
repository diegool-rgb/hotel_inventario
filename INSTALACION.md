# 🚀 Guía de Instalación - Sistema de Inventario Hotelero

## 📋 Para colaboradores y nuevos desarrolladores

### 🔧 **Prerrequisitos**

Antes de comenzar, asegúrate de tener instalado:

1. **Python 3.11+** - [Descargar aquí](https://www.python.org/downloads/)
2. **Git** - [Descargar aquí](https://git-scm.com/downloads)
3. **Un editor de código** (VS Code recomendado)

### 📥 **1. Clonar el Repositorio**

```bash
# Abrir terminal/PowerShell y navegar a donde quieres el proyecto
cd C:\Users\TuUsuario\Documents

# Clonar el repositorio
git clone https://github.com/diegool-rgb/hotel_inventario.git

# Entrar al directorio del proyecto
cd hotel_inventario
```

### 🐍 **2. Crear Entorno Virtual**

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate

# En Linux/Mac:
source .venv/bin/activate
```

**⚠️ Importante**: Siempre activa el entorno virtual antes de trabajar

### 📦 **3. Instalar Dependencias**

```bash
# Instalar todas las dependencias del proyecto
pip install -r requirements.txt
```

### 🗄️ **4. Configurar Base de Datos**

```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar migraciones a la base de datos
python manage.py migrate
```

### 👤 **5. Crear Superusuario**

```bash
# Crear usuario administrador
python manage.py createsuperuser

# Te pedirá:
# - Username: (elige uno)
# - Email: tu-email@example.com
# - Password: (elige una contraseña segura)
```

### 🏨 **6. Cargar Datos del Hotel**

```bash
# Opción 1: Datos básicos de prueba
python data_inicial.py

# Opción 2: Datos reales del hotel (RECOMENDADO)
python poblar_hotel_real.py
```

### 🚀 **7. Ejecutar el Servidor**

```bash
# Iniciar servidor de desarrollo
python manage.py runserver

# El sistema estará disponible en:
# http://127.0.0.1:8000/
```

---

## 🎛️ **Usando los Scripts Automatizados (Windows)**

El proyecto incluye un archivo `comandos.bat` que facilita todas las tareas:

```bash
# Ver todos los comandos disponibles
comandos.bat help

# Comandos más útiles:
comandos.bat servidor    # Iniciar servidor
comandos.bat admin       # Crear superusuario
comandos.bat hotel       # Cargar datos reales del hotel
comandos.bat migraciones # Crear y aplicar migraciones
comandos.bat git         # Subir cambios (para colaboradores)
```

---

## 📁 **Estructura del Proyecto**

```
hotel_inventario/
├── 📁 config/              # Configuración Django
├── 📁 inventario/          # App principal - gestión de inventario
├── 📁 pedidos/            # App de pedidos a proveedores
├── 📁 reportes/           # App de reportes y análisis
├── 📁 usuarios/           # App de gestión de usuarios
├── 📁 templates/          # Templates HTML
├── 📁 static/            # CSS, JS, imágenes
├── 📄 data_inicial.py    # Script datos básicos
├── 📄 poblar_hotel_real.py # Script datos reales del hotel
├── 📄 comandos.bat       # Scripts de automatización
├── 📄 requirements.txt   # Dependencias del proyecto
└── 📄 manage.py         # Comando principal de Django
```

---

## 🌐 **Acceso al Sistema**

### **Página Principal**
- **URL**: http://127.0.0.1:8000/
- **Descripción**: Página de inicio con información del proyecto

### **Panel de Administración**
- **URL**: http://127.0.0.1:8000/admin/
- **Usuario**: El que creaste en el paso 5
- **Funciones**: Gestión completa de datos

### **Dashboard Principal**
- **URL**: http://127.0.0.1:8000/inventario/
- **Descripción**: Panel principal del sistema

---

## 🔧 **Desarrollo y Colaboración**

### **Hacer Cambios**

```bash
# 1. Activar entorno virtual
.venv\Scripts\activate

# 2. Hacer tus cambios en el código

# 3. Probar que funciona
python manage.py runserver

# 4. Subir cambios (usando script automatizado)
comandos.bat git

# O manualmente:
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

### **Mantener Actualizado**

```bash
# Obtener últimos cambios del repositorio
git pull origin main

# Si hay nuevas dependencias
pip install -r requirements.txt

# Si hay nuevas migraciones
python manage.py migrate
```

---

## 🚨 **Solución de Problemas Comunes**

### **Error: "python no se reconoce"**
- Instala Python desde python.org
- Asegúrate de marcar "Add to PATH" en la instalación

### **Error: "No module named django"**
- Activa el entorno virtual: `.venv\Scripts\activate`
- Instala dependencias: `pip install -r requirements.txt`

### **Error de migraciones**
```bash
# Resetear migraciones si es necesario
python manage.py migrate --run-syncdb
```

### **Error de permisos en Windows**
- Ejecuta PowerShell como administrador
- O usa: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 📞 **Soporte**

Si tienes problemas:

1. **Revisa esta guía** paso a paso
2. **Verifica los prerrequisitos** (Python, Git)
3. **Contacta al desarrollador**: dg1604719@gmail.com
4. **Crear Issue en GitHub**: [Reportar problema](https://github.com/diegool-rgb/hotel_inventario/issues)

---

## 🎯 **Resumen Rápido para Expertos**

```bash
git clone https://github.com/diegool-rgb/hotel_inventario.git
cd hotel_inventario
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python poblar_hotel_real.py
python manage.py runserver
```

¡Listo! El sistema estará corriendo en http://127.0.0.1:8000/ 🚀
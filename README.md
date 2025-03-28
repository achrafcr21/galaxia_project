# Proyecto Galaxia - Sistema de Procesamiento de Documentos

## Descripción
Sistema de procesamiento de documentos construido con Django que permite la carga y procesamiento asíncrono de archivos PDF, Excel y Word. Utiliza Celery con Redis para el procesamiento en segundo plano y PostgreSQL como base de datos.

## Características Principales
- Carga de documentos (PDF, Excel, Word)
- Procesamiento asíncrono de documentos
- Extracción de texto y metadata
- Interfaz de administración Django
- API REST para carga de documentos
- Sistema de colas con Celery y Redis

## Requisitos del Sistema
- Python 3.11+
- PostgreSQL
- Redis (Memurai para Windows)
- Dependencias Python (ver requirements.txt)

## Estructura del Proyecto
```
Proyecto_Galaxia/
├── config/                 # Configuración principal del proyecto
│   ├── __init__.py
│   ├── celery.py          # Configuración de Celery
│   ├── settings.py        # Configuración de Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py
├── galaxia_app/           # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas y endpoints
│   ├── admin.py           # Configuración del admin
│   ├── tasks.py           # Tareas de Celery
│   └── services/          # Servicios y utilidades
│       └── document_processor.py
├── media/                 # Archivos subidos
├── static/                # Archivos estáticos
├── manage.py
└── requirements.txt       # Dependencias del proyecto
```

## Configuración del Entorno

1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd Proyecto_Galaxia
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

## Ejecución del Proyecto

1. Iniciar Redis (Memurai en Windows)

2. Iniciar el servidor Django:
```bash
python manage.py runserver
```

3. Iniciar el worker de Celery:
```bash
celery -A config worker --pool=solo -l info
```

## Uso del Sistema

### Panel de Administración
- Acceder a `http://localhost:8000/admin/`
- Iniciar sesión con credenciales de superusuario
- Navegar a la sección "Documentos"
- Usar el botón "Add Documento" para subir archivos

### API REST
Endpoint para subir documentos:
```
POST /documentos/upload/
```

## Modelo de Datos

### Documento
- usuario: Usuario que subió el documento
- titulo: Título del documento
- archivo: Archivo subido
- formato: Tipo de archivo
- contenido_procesado: Contenido extraído (JSON)
- resumen_ia: Resumen generado por IA
- categorias_ia: Categorías asignadas por IA
- fecha_procesado: Fecha de procesamiento
- fecha_creacion: Fecha de creación
- fecha_actualizacion: Última actualización

## Procesamiento de Documentos
El sistema procesa automáticamente los documentos subidos:
1. El documento se sube a través del admin o API
2. Se encola una tarea en Celery
3. El worker procesa el documento en segundo plano
4. Se extraen texto y metadata
5. Se actualiza el registro en la base de datos

## Configuración Actual
- Django: Configurado con PostgreSQL
- Celery: Usando Redis como broker
- Almacenamiento: Sistema de archivos local
- Procesamiento: Asíncrono con workers de Celery

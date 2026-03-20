from datetime import timedelta  # Importa `timedelta` para configurar duraciones (p. ej., JWT).
import os  # Acceso a variables de entorno y utilidades del sistema operativo.
import sys  # Acceso a argumentos/flags del proceso (util para detectar `test`).

from pathlib import Path  # Manejo de rutas de forma portable.

BASE_DIR = Path(__file__).resolve().parent.parent  # Ruta base del proyecto (dos niveles arriba de este archivo).


# Clave secreta de Django (en produccion debe venir desde variables de entorno).
SECRET_KEY = 'django-insecure-+^r^8axypcaff45vn7y9v#i=#oab1#18tn0%n(%nika5knpbqv'  # Clave secreta usada por Django para firmas/crypto.


DEBUG = True  # Activa modo debug (no recomendado en produccion).

ALLOWED_HOSTS = [  # Lista de hosts/dominios permitidos para servir la app.
    "localhost",  # Acceso local por nombre.
    "192.168.1.3",  # IP local (red LAN) autorizada.
    "127.0.0.1",  # Loopback IPv4.
    "10.0.2.2",  # IP tipica para emuladores (Android) hacia host.
    "0.0.0.0",  # Binding generico (util en contenedores/dev).
]  # Fin de `ALLOWED_HOSTS`.



# Application definition

INSTALLED_APPS = [  # Apps instaladas (Django + terceros + propias).
    'django.contrib.admin',  # Admin de Django.
    'django.contrib.auth',  # Autenticacion/usuarios.
    'django.contrib.contenttypes',  # Tipos de contenido.
    'django.contrib.sessions',  # Sesiones.
    'django.contrib.messages',  # Mensajes flash.
    'django.contrib.staticfiles',  # Manejo de estaticos.

    'rest_framework',  # Django REST Framework.
    'corsheaders',  # Soporte para CORS.
    'app',  # App propia del proyecto.
]  # Fin de `INSTALLED_APPS`.

MIDDLEWARE = [  # Middlewares ejecutados en cada request/response.
    'corsheaders.middleware.CorsMiddleware',  # Inyecta cabeceras CORS.
    'django.middleware.security.SecurityMiddleware',  # Cabeceras de seguridad.
    'django.contrib.sessions.middleware.SessionMiddleware',  # Soporte de sesion.
    'django.middleware.common.CommonMiddleware',  # Utilidades comunes (ETag, etc.).
    'django.middleware.csrf.CsrfViewMiddleware',  # Proteccion CSRF.
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Autenticacion en request.
    'django.contrib.messages.middleware.MessageMiddleware',  # Mensajeria.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Mitiga clickjacking.
]  # Fin de `MIDDLEWARE`.

CORS_ALLOW_ALL_ORIGINS = True  # Permite CORS desde cualquier origen (para dev; ajustar en prod).

ROOT_URLCONF = 'api_wini.urls'  # Modulo principal de URLs del proyecto.

TEMPLATES = [  # Configuracion de templates (Django Templates).
    {  # Un motor de templates.
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Backend del motor.
        'DIRS': [],  # Directorios extra de templates (vacio = ninguno).
        'APP_DIRS': True,  # Busca templates dentro de cada app instalada.
        'OPTIONS': {  # Opciones del motor.
            'context_processors': [  # Procesadores de contexto habilitados.
                'django.template.context_processors.request',  # Agrega `request` al contexto.
                'django.contrib.auth.context_processors.auth',  # Agrega `user` y auth context.
                'django.contrib.messages.context_processors.messages',  # Agrega mensajes al contexto.
            ],  # Fin de `context_processors`.
        },  # Fin de `OPTIONS`.
    },  # Fin del motor.
]  # Fin de `TEMPLATES`.

# Configuracion global de DRF: exige JWT (Bearer token) en endpoints protegidos.
REST_FRAMEWORK = {  # Configuracion global de Django REST Framework.
    'DEFAULT_AUTHENTICATION_CLASSES': [  # Clases de autenticacion por defecto.
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Autenticacion JWT (Bearer).
    ],  # Fin de `DEFAULT_AUTHENTICATION_CLASSES`.
}  # Fin de `REST_FRAMEWORK`.

SIMPLE_JWT = {  # Configuracion de SimpleJWT (tokens).
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Vigencia del access token.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Vigencia del refresh token.
    'AUTH_HEADER_TYPES': ('Bearer',),  # Prefijo esperado en Authorization header.
}  # Fin de `SIMPLE_JWT`.





WSGI_APPLICATION = 'api_wini.wsgi.application'  # Punto de entrada WSGI (deploy tradicional).


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {  # Configuracion de bases de datos.
    'default': {  # Conexion por defecto.
        'ENGINE': 'django.db.backends.postgresql',  # Motor PostgreSQL.
        'NAME': 'app_wini',  # Nombre de la base de datos.
        'USER': 'guayabal_user',  # Usuario de la base de datos.
        'PASSWORD': 'admin1234',  # Contrasena de la base de datos.
        'HOST': 'localhost',  # Host del servidor de BD.
        'PORT': '5432',  # Puerto del servidor de BD.
    }  # Fin de conexion `default`.
}  # Fin de `DATABASES`.

# Evita requerir CREATEDB en PostgreSQL al correr tests locales.
IS_TESTING = any(arg.startswith('test') for arg in sys.argv)  # Detecta si el comando actual es de tests.
USE_SQLITE_FOR_TESTS = os.getenv('USE_SQLITE_FOR_TESTS', '1').strip().lower() in {'1', 'true', 'yes'}  # Flag para usar SQLite en tests.
if IS_TESTING and USE_SQLITE_FOR_TESTS:  # Si se estan corriendo tests y esta habilitado SQLite...
    DATABASES['default'] = {  # Sobrescribe la BD por defecto para tests.
        'ENGINE': 'django.db.backends.sqlite3',  # Motor SQLite (rapido y sin servidor).
        'NAME': ':memory:',  # Base en memoria para tests.
    }  # Fin de override `DATABASES['default']`.


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [  # Validadores de contrasenas para `User`.
    {  # Valida similitud con atributos del usuario.
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Similaridad usuario/atributos.
    },  # Fin del validador 1.
    {  # Valida longitud minima.
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Longitud minima.
    },  # Fin del validador 2.
    {  # Bloquea contrasenas comunes.
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Contrasenas comunes.
    },  # Fin del validador 3.
    {  # Evita contrasenas puramente numericas.
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Solo numeros.
    },  # Fin del validador 4.
]  # Fin de `AUTH_PASSWORD_VALIDATORS`.


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'es-mx'  # Idioma por defecto de la app.

TIME_ZONE = 'UTC'  # Zona horaria del proyecto.

USE_I18N = True  # Habilita internacionalizacion.

USE_TZ = True  # Habilita datetimes con timezone.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'  # URL base para archivos estaticos.

MEDIA_URL = '/media/'  # URL base para servir archivos subidos.
MEDIA_ROOT = BASE_DIR / 'media'  # Carpeta donde se guardan archivos subidos.

# Google Maps/Places server key (use backend-only key restricted by IP).
GOOGLE_MAPS_SERVER_API_KEY = os.getenv('GOOGLE_MAPS_SERVER_API_KEY', '')  # API key (backend) para Google Maps/Places.
GOOGLE_MAPS_LANGUAGE = os.getenv('GOOGLE_MAPS_LANGUAGE', 'es')  # Idioma preferido para resultados de Google.
GOOGLE_MAPS_REGION = os.getenv('GOOGLE_MAPS_REGION', 'ec')  # Region preferida para resultados de Google.

# Geo provider:
# - "osm": OpenStreetMap stack (Nominatim + OSRM) [default]
# - "google": Google stack (Places/Geocoding/Routes/Address Validation)
GEO_PROVIDER = os.getenv('GEO_PROVIDER', 'osm').strip().lower()  # Proveedor geografico seleccionado (`osm` o `google`).

# OpenStreetMap / OSRM settings
GEOCODER_USER_AGENT = os.getenv('GEOCODER_USER_AGENT', 'api-guayabal/1.0 (mobile-app)')  # User-Agent para Nominatim.
OSM_NOMINATIM_BASE_URL = os.getenv('OSM_NOMINATIM_BASE_URL', 'https://nominatim.openstreetmap.org')  # Base URL de Nominatim.
OSM_ROUTER_BASE_URL = os.getenv('OSM_ROUTER_BASE_URL', 'https://router.project-osrm.org')  # Base URL de OSRM (ruteo).

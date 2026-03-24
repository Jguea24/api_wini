# Informe Tecnico - API Guayabal (`api_wini`)

Fecha del informe: 23 de marzo de 2026  
Tipo de sistema: Backend REST para ecommerce y trazabilidad de chocolate  
Framework principal: Django + Django REST Framework

## 1. Resumen Ejecutivo

`api_wini` es una API REST desarrollada en Django que soporta el flujo operativo de una aplicacion de comercio electronico. El sistema incluye autenticacion JWT, catalogo de productos, carrito, pedidos, direcciones, seguimiento logistica de envios, solicitudes de cambio de rol y trazabilidad por codigo QR para lotes de chocolate.

El backend tambien incluye un panel administrativo personalizado (`/admin/`) con dashboard de metricas operativas y de negocio.

## 2. Objetivo del Sistema

- Centralizar la gestion de usuarios, productos y pedidos.
- Exponer endpoints para la app movil/web.
- Permitir geolocalizacion, validacion de direcciones y estimacion de rutas.
- Soportar trazabilidad de lotes desde QR para transparencia del producto.

## 3. Alcance Funcional

### 3.1 Modulos implementados

- Autenticacion y perfil de usuario (`register`, `login`, `me`, cambio de password).
- Catalogo comercial (banners, categorias y productos).
- Carrito de compras (crear, actualizar, eliminar, conteo).
- Pedidos y envios (creacion, seguimiento, asignacion de repartidor, ubicacion).
- Direcciones de entrega por usuario.
- Solicitudes de rol (`driver` y `provider`) con flujo de aprobacion.
- Geoservicios (`autocomplete`, `geocode`, validacion de direccion, rutas).
- Trazabilidad por QR de lotes de chocolate.
- Dashboard administrativo con indicadores.

### 3.2 Fuera de alcance actual

- Motor de pagos integrado.
- Pipeline CI/CD definido en repositorio.
- Suite de pruebas extensa por modulo (actualmente solo chequeos basicos).

## 4. Arquitectura Tecnica

- Lenguaje: Python 3.12+
- Framework web: Django 6
- API: Django REST Framework
- Auth: SimpleJWT (Bearer Token)
- Base de datos principal: PostgreSQL
- Base de datos para tests (opcional): SQLite en memoria
- Librerias clave: `django-cors-headers`, `Pillow`
- Integraciones de mapas: OpenStreetMap/OSRM o Google Maps Platform

### 4.1 Versiones usadas en el entorno actual

Versiones verificadas en el entorno local (23 de marzo de 2026):

- Python: `3.12.10`
- Django: `6.0.1`
- Django REST Framework: `3.16.1`
- SimpleJWT (`djangorestframework_simplejwt`): `5.5.1`
- `django-cors-headers`: `4.9.0`
- Pillow: `12.1.1`
- `psycopg2-binary`: `2.9.11`
- Motor de base de datos (instancia local): PostgreSQL `18.1`

### 4.2 Estructura del proyecto

```text
api_wini/
  api_wini/                  # settings, urls, wsgi, asgi
  app/                       # modelos, vistas, serializers, admin, permisos
  app/templates/admin/       # dashboard administrativo
  media/                     # archivos subidos (imagenes)
  manage.py
  README.md
```

## 5. Modelo de Dominio (Resumen)

Entidades principales:

- Catalogo: `Category`, `Banner`, `Product`
- Usuario y perfil: `UserProfile`
- Compra: `Cart`, `Order`, `OrderItem`
- Entrega: `DeliveryAddress`, `Shipment`, `ShipmentLocation`
- Roles: `RoleChangeRequest`
- Trazabilidad: `CocoaInfo`, `ChocolateLot`, `LotTraceEvent`

## 6. Endpoints Principales

Base URL local: `http://127.0.0.1:8000/`

### 6.1 Publicos

- `GET /`
- `POST /register/`
- `GET /register/`
- `POST /login/`
- `POST /token/refresh/`
- `GET /banners/`
- `GET /categories/`
- `GET /products/`
- `GET /products/<id>/`
- `GET /trace/qr/<qr_code>/`

### 6.2 Protegidos (Bearer Token)

- `GET /me/`
- `PATCH /me/`
- `POST /me/change-password/`
- `GET|POST|PATCH|DELETE /cart/`
- `GET /cart/count/`
- `GET|POST /orders/`
- `GET /orders/<id>/`
- `GET /orders/<id>/tracking/`
- `POST /orders/<id>/tracking/assign-driver/`
- `POST /orders/<id>/tracking/location/`
- `GET|POST /addresses/`
- `GET|PATCH|DELETE /addresses/<id>/`
- `GET|POST /role-requests/`
- `GET /geo/autocomplete/`
- `GET /geo/geocode/`
- `POST /geo/validate-address/`
- `POST /geo/routes/estimate/`

### 6.3 Administrativo

- `GET /admin/` (dashboard personalizado)

## 7. Flujo de Autenticacion JWT

1. Registrar usuario en `POST /register/`.
2. Iniciar sesion en `POST /login/`.
3. Recibir `access` y `refresh`.
4. Consumir endpoints privados con header:

```http
Authorization: Bearer <access_token>
```

5. Renovar token en `POST /token/refresh/`.

## 8. Configuracion y Variables de Entorno

Archivo clave: `api_wini/settings.py`

### 8.1 Base de datos y conexion actual

Configuracion activa observada en `settings.py`:

- Engine: `django.db.backends.postgresql`
- Database: `app_wini`
- User: `guayabal_user`
- Host: `localhost`
- Port: `5432`
- Driver Python: `psycopg2-binary 2.9.11`
- Version del servidor validada: PostgreSQL `18.1`

Ejemplo equivalente de cadena de conexion:

```text
postgresql://guayabal_user:admin1234@localhost:5432/app_wini
```

Variables usadas en geolocalizacion:

- `GEO_PROVIDER` (`osm` o `google`)
- `GOOGLE_MAPS_SERVER_API_KEY`
- `GOOGLE_MAPS_LANGUAGE`
- `GOOGLE_MAPS_REGION`
- `GEOCODER_USER_AGENT`
- `OSM_NOMINATIM_BASE_URL`
- `OSM_ROUTER_BASE_URL`

Notas actuales observadas en configuracion local:

- `DEBUG=True`
- `CORS_ALLOW_ALL_ORIGINS=True`
- Credenciales de BD hardcodeadas en settings

## 9. Ejecucion Local (Windows / PowerShell)

1. Crear entorno virtual:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers psycopg2-binary pillow
```

3. Aplicar migraciones:

```powershell
python manage.py migrate
```

4. Ejecutar servidor:

```powershell
python manage.py runserver
```

## 10. Verificacion Tecnica

Chequeo ejecutado:

```powershell
python manage.py check
```

Resultado: `System check identified no issues (0 silenced).`

## 11. Riesgos y Recomendaciones

- Mover `SECRET_KEY` y credenciales de DB a variables de entorno.
- Desactivar `DEBUG` en produccion.
- Restringir CORS por dominios permitidos.
- Agregar `requirements.txt` o `pyproject.toml` para versionado de dependencias.
- Incorporar pruebas automatizadas por modulo critico (auth, orders, tracking).
- Definir pipeline CI/CD para validacion y despliegue.

## 12. Estado General

El sistema se encuentra operativo en entorno local, con modulos principales funcionales para ecommerce, logistica y trazabilidad. La base tecnica es adecuada para evolucionar a un entorno de produccion, condicionada a mejoras de seguridad, observabilidad y automatizacion.

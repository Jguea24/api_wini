# API Guayabal (api_wini)

Backend REST construido con Django + Django REST Framework para autenticacion JWT, catalogo de productos, carrito, pedidos, direcciones y seguimiento.

## Stack

- Python 3.12+
- Django 6
- Django REST Framework
- SimpleJWT
- PostgreSQL
- Pillow
- django-cors-headers

## Modulos principales

- Autenticacion y usuarios (`register`, `login`, `me`, cambio de password)
- Catalogo (`banners`, `categories`, `products`)
- Carrito (`cart`, `cart/count`)
- Pedidos y tracking (`orders`, tracking de envio, asignacion de repartidor)
- Direcciones de entrega (`addresses`)
- Solicitudes de rol (`role-requests`)
- Geocoding y rutas (`geo/*`)

## Estructura basica

```text
api_wini/
- api_guayabal/      # settings, urls, wsgi, asgi
- app/               # models, serializers, views, admin, permissions
- media/             # archivos cargados (imagenes)
- manage.py
```

## Instalacion local

1. Crear y activar entorno virtual:

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

4. Levantar servidor:

```powershell
python manage.py runserver
```

## Configuracion

Archivo principal: `api_guayabal/settings.py`

- Base de datos por defecto: PostgreSQL (`DATABASES`)
- JWT global en DRF:
  - `DEFAULT_AUTHENTICATION_CLASSES = JWTAuthentication`
  - `AUTH_HEADER_TYPES = ('Bearer',)`
- Lifetimes:
  - Access token: 60 minutos
  - Refresh token: 1 dia

Variables de entorno usadas por geolocalizacion:

- `GOOGLE_MAPS_SERVER_API_KEY`
- `GOOGLE_MAPS_LANGUAGE`
- `GOOGLE_MAPS_REGION`
- `GEO_PROVIDER` (`osm` o `google`)
- `GEOCODER_USER_AGENT`
- `OSM_NOMINATIM_BASE_URL`
- `OSM_ROUTER_BASE_URL`

## Flujo de autenticacion JWT

1. Registrar usuario: `POST /register/`
2. Iniciar sesion: `POST /login/`
3. Recibir `access` y `refresh`
4. Consumir rutas protegidas con:

```http
Authorization: Bearer <access_token>
```

5. Renovar access token: `POST /token/refresh/`

## Endpoints principales

### Auth

- `POST /register/` (crea usuario)
- `GET /register/` (lista usuarios registrados)
- `POST /login/`
- `POST /token/refresh/`
- `GET /me/`
- `PATCH /me/`
- `POST /me/change-password/`

### Publicos

- `GET /banners/`
- `GET /categories/`
- `GET /products/`
- `GET /products/<id>/`

### Protegidos (Bearer token)

- `GET|POST|PATCH|DELETE /cart/`
- `GET /cart/count/`
- `GET|POST /orders/`
- `GET /orders/<id>/`
- `GET /orders/<id>/tracking/`
- `POST /orders/<id>/tracking/location/`
- `POST /orders/<id>/tracking/assign-driver/`
- `GET|POST /addresses/`
- `GET|PATCH|DELETE /addresses/<id>/`
- `GET|POST /role-requests/`
- `GET /geo/autocomplete/`
- `GET /geo/geocode/`
- `POST /geo/validate-address/`
- `POST /geo/routes/estimate/`

## Ejemplo rapido

Login:

```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"usuario\",\"password\":\"12345678\"}"
```

Consultar perfil autenticado:

```bash
curl http://127.0.0.1:8000/me/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN"
```

## Comando de verificacion

```powershell
python manage.py check
```

## Notas de seguridad (recomendado para produccion)

- No dejar `DEBUG=True`.
- No exponer `SECRET_KEY` en repositorio.
- Restringir CORS a dominios confiables.
- Mover credenciales de base de datos a variables de entorno.

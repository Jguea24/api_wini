# ASGI config for api_wini project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/

import os  # Importa os.

from django.core.asgi import get_asgi_application  # Importa get_asgi_application desde `django.core.asgi`.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_wini.settings')  # Define la variable de entorno `DJANGO_SETTINGS_MODULE` si no existe.

application = get_asgi_application()  # Asigna a `application` el resultado de `get_asgi_application`.

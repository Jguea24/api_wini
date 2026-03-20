# WSGI config for api_wini project.
#
# It exposes the WSGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/

import os  # Importa os.

from django.core.wsgi import get_wsgi_application  # Importa get_wsgi_application desde `django.core.wsgi`.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_wini.settings')  # Define la variable de entorno `DJANGO_SETTINGS_MODULE` si no existe.

application = get_wsgi_application()  # Asigna a `application` el resultado de `get_wsgi_application`.

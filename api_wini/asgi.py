# ASGI config for api_wini project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/

import os  # comentario

from django.core.asgi import get_asgi_application  # comentario

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_wini.settings')  # comentario

application = get_asgi_application()  # comentario

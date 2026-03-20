# WSGI config for api_wini project.
#
# It exposes the WSGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/

import os  # comentario

from django.core.wsgi import get_wsgi_application  # comentario

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_wini.settings')  # comentario

application = get_wsgi_application()  # comentario

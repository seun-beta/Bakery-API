"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from core.settings.base import SETTINGS_FILE

os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)

application = get_wsgi_application()

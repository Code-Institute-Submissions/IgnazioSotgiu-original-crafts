"""
WSGI config for original_crafts project.

"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'original_crafts.settings')

application = get_wsgi_application()

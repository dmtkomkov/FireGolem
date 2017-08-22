import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/FireGolem')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FireGolem.settings")

application = get_wsgi_application()

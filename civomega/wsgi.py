import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "civomega.settings_live")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

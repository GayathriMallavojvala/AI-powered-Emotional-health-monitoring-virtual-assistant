import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mental_Health_Support.settings')

application = get_wsgi_application()

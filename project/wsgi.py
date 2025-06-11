import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# غير 'application' إلى 'app'
app = get_wsgi_application()
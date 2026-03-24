# wsgi.py - Place this in your project root on PythonAnywhere
import os
import sys

# Add your project directory to the path
path = '/home/yourusername/church-registry-system'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
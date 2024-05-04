 
import os, sys
sys.path.insert(0, '/root/projects/glossy-habit-tracker-backend')
sys.path.insert(1, '/root/projects/glossy-habit-tracker-backend/venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'habbit.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
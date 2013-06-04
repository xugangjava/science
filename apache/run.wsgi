import os, sys
sys.path.append(r'C:\science')
os.environ['DJANGO_SETTINGS_MODULE'] = 'science.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
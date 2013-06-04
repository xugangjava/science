#coding=utf-8
# Django settings for science project.



DEBUG = True
TEMPLATE_DEBUG = DEBUG
FCGI_DEBUG=False
from os.path import dirname, join,abspath
from tools import const
import  sitecustomize
const.Const.DEBUG=DEBUG


HERE=abspath(join(dirname( __file__ ), '..')).replace('\\','/')
const.Const.HERE=HERE
ADMINS = (
# ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

#sqlite
DATABASES = {
    'default': {
        #'ENGINE': 'doj.backends.zxjdbc.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': HERE+'/science.db', # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        #'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}


#msql
#DATABASES = {
#	'default': {
#		#'ENGINE': 'doj.backends.zxjdbc.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#		'ENGINE': 'django.db.backends.mysql',
#		'NAME': 'science', # Or path to database file if using sqlite3.
#		'USER': 'root', # Not used with sqlite3.
#		'PASSWORD': '0000', # Not used with sqlite3.
#		#'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
#                'HOST': '127.0.0.1', # Set to empty string for localhost. Not used with sqlite3.
#		'PORT': '3306', # Set to empty string for default. Not used with sqlite3.
#	}
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT =HERE+'/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/resources/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = 'C:/quick/Projects/science/static/'

STATIC_ROOT =join(HERE,'static')


SITE_STATIC_ROOT=join(STATIC_ROOT,'ext')
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
SITE_STATIC_ROOT,
)



# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
	)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!crcv(r9&amp;8&amp;ar_y69eix6@7%79-%+yft19vad5mp_ix*0zd)=1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',

	#     'django.template.loaders.eggs.Loader',
	)



MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	# Uncomment the next line for simple clickjacking protection:
	# 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'tools.const.DisableCSRF'
	)

ROOT_URLCONF = 'science.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'science.wsgi.application'

TEMPLATE_DIRS = (HERE+'/templates',)


#
#import djcelery
#djcelery.setup_loader()

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	# 'django.contrib.admindocs',
	'core',

	#'djcelery',
        'south'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'formatters': {
		'verbose': {
			'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
		},
		'simple': {
			'format': '%(levelname)s %(message)s'
		},
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		},
		'console':{
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
	},

	'loggers': {
#		'django.request': {
#			'handlers': ['mail_admins'],
#			'level': 'ERROR',
#			'propagate': True,
#		},

		'django.db.backends': {
			'handlers': ['mail_admins'],
			'propagate': True,
			'level':'DEBUG',
			},
		}
}




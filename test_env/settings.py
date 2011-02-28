import os, sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, '..'))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'test.db',
	}
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

INSTALLED_APPS = (
	'django_mathlatex',
)

MATHLATEX_IMAGES_DIR = 'math/'

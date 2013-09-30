# Dev-only settings for battleforboston website.
from defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3', 
    'NAME': os.path.join(BASE_DIR, '../test.db'),
    # The following settings are not used with sqlite3:
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
  }
}

SECRET_KEY = 'secret'

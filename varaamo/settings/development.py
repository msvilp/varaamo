"""
Settings for local development.
"""

from .base import *  # noqa: F403, F401
import os

ALLOWED_HOSTS = ["*"]
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'varaamo'),
        'USER': os.environ.get('MYSQL_USER', 'varaamo'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'varaamo'),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

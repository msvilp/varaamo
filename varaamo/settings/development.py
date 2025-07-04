"""
Settings for local development.
"""
# pylint: disable=wildcard-import,unused-wildcard-import
import os

from .base import *  # noqa: F403, F401

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ["http://localhost:8030"]
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

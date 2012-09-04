### -*- coding: utf-8 -*- ###
try:
    from django.conf import settings
except ImportError:
    settings = object

TOMBOY_DOMAIN = getattr(settings, 'TOMBOY_DOMAIN', 'https://one.ubuntu.com/notes/')
API_VERSION = getattr(settings, 'API_VERSION', '1.0')

TOMBOY_KEY = getattr(settings, 'TOMBOY_KEY', 'ubuntuone')
TOMBOY_SECRET = getattr(settings, 'TOMBOY_SECRET', 'hammertime')
TOMBOY_SIGNATURE_METHOD = getattr(settings, 'TOMBOY_SIGNATURE_METHOD', 'PLAINTEXT')
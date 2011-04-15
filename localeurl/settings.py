import re
from django.conf import settings

SUPPORTED_LOCALES = dict(settings.LANGUAGES)
# Sort locale codes longest-first to avoid matching e.g. 'nl' before 'nl-be'
LOCALES_RE = '|'.join(
    sorted(SUPPORTED_LOCALES.keys(), key=lambda i: len(i), reverse=True))
PATH_RE = re.compile(r'^/(?P<locale>%s)(?P<path>.*)$' % LOCALES_RE)

LOCALE_INDEPENDENT_PATHS = getattr(settings, 'LOCALE_INDEPENDENT_PATHS', ())

LOCALE_INDEPENDENT_MEDIA_URL = getattr(settings,
        'LOCALE_INDEPENDENT_MEDIA_URL', True)

LOCALE_INDEPENDENT_STATIC_URL = getattr(settings,
        'LOCALE_INDEPENDENT_STATIC_URL', True)

PREFIX_DEFAULT_LOCALE = getattr(settings, 'PREFIX_DEFAULT_LOCALE', True)

USE_ACCEPT_LANGUAGE = getattr(settings, 'LOCALEURL_USE_ACCEPT_LANGUAGE', False)

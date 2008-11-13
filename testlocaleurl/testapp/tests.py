"""
Tests for the localeurl application.

Module utils:

    >>> from localeurl.utils import *

    >>> is_locale_independent('/nl/about')
    False
    >>> is_locale_independent('/media/img/logo.png')
    True
    >>> is_locale_independent('/')
    True
    >>> is_locale_independent('/test/independent/bla/bla')
    True

    >>> strip_locale_prefix('/')
    '/'
    >>> strip_locale_prefix('/about/')
    '/about/'
    >>> strip_locale_prefix('/about/localeurl/')
    '/about/localeurl/'
    >>> strip_locale_prefix('/fr/about/localeurl/')
    '/about/localeurl/'
    >>> strip_locale_prefix('/en-gb/about/localeurl/')
    '/about/localeurl/'
    >>> strip_locale_prefix('/pl/about/localeurl/')
    '/pl/about/localeurl/'

Module middleware:

    >>> from django.test.client import Client
    >>> c = Client()
    >>> r = c.get('/test/')
    >>> r.status_code
    302
    >>> r['Location'] == 'http://testserver/en-us/test/'
    True

    >>> r = c.get('/fr/test/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'fr'
    True

    >>> r = c.get('/en-us/test/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'en-us'
    True

    >>> r = c.get('/test/independent/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'en-us'
    True

    >>> r = c.get('/test/independent/extra/path/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'en-us'
    True

    >>> r = c.get('/en-gb/test/independent/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'en-gb'
    True

Template tags and filters:

    >>> r = c.get('/nl/test/locale_url/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /nl/test/dummy/ \\n /en-us/test/dummy/4 \\n /fr/test/dummy/4 \\n'

    >>> r = c.get('/nl/test/chlocale/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /fr/admin/ \\n /en-gb/admin/ \\n /nl/admin/ \\n'

    >>> r = c.get('/nl/test/rmlocale/')
    >>> r.status_code
    200
    >>> r.content
    '\\n /admin/ \\n /admin/ \\n /admin/ \\n'

Test REDIRECT_LOCALE_INDEPENDENT_PATHS:

    (Changing the settings at runtime is a bit of a hack.)
    >>> from localeurl import middleware
    >>> middleware.REDIRECT_LOCALE_INDEPENDENT_PATHS = True

    >>> r = c.get('/en-us/test/independent/')
    >>> r.status_code
    302
    >>> r['Location'] == 'http://testserver/test/independent/'
    True

    >>> r = c.get('/test/independent/')
    >>> r.status_code
    200
    >>> r.context['LANGUAGE_CODE'] == 'en-us'
    True

"""

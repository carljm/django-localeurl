# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
import localeurl
from localeurl.utils import is_locale_independent, get_language

def reverse(viewname, urlconf=None, args=[], kwargs={}, prefix=None):
    locale = get_language(kwargs.pop('locale', translation.get_language()))
    path = django_reverse(viewname, urlconf, args, kwargs, prefix)
    if not settings.USE_I18N:
        return path
    if not localeurl.PREFIX_DEFAULT_LOCALE \
            and locale == get_language(settings.LANGUAGE_CODE):
        return path
    script_prefix = urlresolvers.get_script_prefix()
    path = script_prefix + locale + '/' + path[len(script_prefix):]
    return path

django_reverse = urlresolvers.reverse
urlresolvers.reverse = reverse

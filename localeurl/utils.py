# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

import re
from django.conf import settings
from django.core import urlresolvers
import localeurl.settings

SUPPORTED_LOCALES = dict(settings.LANGUAGES)
LOCALES_RE = '|'.join(SUPPORTED_LOCALES)
PATH_RE = re.compile(r'^/(?P<locale>%s)(?P<path>.*)$' % LOCALES_RE)
DOMAIN_RE = re.compile(r'^(?P<locale>%s)\.(?P<domain>.*)$' % LOCALES_RE)

def is_locale_independent(path):
    """
    Returns whether the path is locale-independent.

    A path is independent if it starts with MEDIA_URL or it is matched by any
    pattern from LOCALE_INDEPENDENT_PATHS.
    """
    if settings.MEDIA_URL and path.startswith(settings.MEDIA_URL):
        return True
    for re in localeurl.settings.LOCALE_INDEPENDENT_PATHS:
        if re.search(path):
            return True
    return False

def strip_path(path):
    """
    Returns the path without the locale prefix. If the path does not begin
    with a locale it is returned without change. The path must contain the
    script prefix.
    """
    check = PATH_RE.match(path)
    if check:
        return check.group('locale'), check.group('path')
    else:
        return '', path

def strip_domain(domain):
    """
    Returns the domain without the locale component. If the domain does not
    begin with a locale it is returned without change.
    """
    check = DOMAIN_RE.match(domain)
    if check:
        return check.group('locale'), check.group('domain')
    else:
        return '', domain

def supported_language(locale):
    """
    Returns the supported language (from settings.LANGUAGES) for the locale.
    """
    if locale in SUPPORTED_LOCALES:
        return locale
    elif locale[:2] in SUPPORTED_LOCALES:
        return locale[:2]
    else:
        return None

def is_default_locale(locale):
    """
    Returns whether the locale is the default locale.
    """
    return locale == supported_language(settings.LANGUAGE_CODE)

def locale_path(path, locale=''):
    """
    Generate the localeurl-enabled path from a path without locale prefix. If
    the locale is empty settings.LANGUAGE_CODE is used.
    """
    if not locale:
        locale = supported_language(settings.LANGUAGE_CODE)
    if localeurl.settings.URL_TYPE == 'domain_prefix':
        return path
    elif is_locale_independent(path):
        return path
    elif is_default_locale(locale) \
            and not localeurl.settings.PREFIX_DEFAULT_LOCALE:
        return path
    else:
        return ''.join([u'/', locale, path])

def locale_url(path, locale=''):
    """
    Generate the localeurl-enabled URL from a path without locale prefix. If
    the locale is empty settings.LANGUAGE_CODE is used.
    """
    path = locale_path(path, locale)
    return ''.join([urlresolvers.get_script_prefix(), path[1:]])

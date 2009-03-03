# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

import re
from django.conf import settings as django_settings
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from localeurl.resolver.base import Resolver

PATH_PATTERN = r'^/(?P<locale>%s)(?P<path>.*)$'

class PathPrefixResolver(Resolver):
    """
    Localeurl resolver that sets the language based on the request path prefix
    and strips that prefix from the path. It will also automatically redirect
    any path without a prefix, unless PREFIX_DEFAULT_LOCALE is set to True.
    Exceptions are paths beginning with MEDIA_URL or matching any regular
    expression from LOCALE_INDEPENDENT_PATHS from the project settings.

    For example, the path '/en/admin/' will set request.LANGUAGE_CODE to 'en'
    and request.path to '/admin/'.

    Alternatively, the language is set by the first component of the domain
    name. For example, a request on 'fr.example.com' would set the language to
    French.

    If you use this middleware the django.core.urlresolvers.reverse function
    is be patched to return paths with locale prefix.
    """

    def __init__(self, settings=django_settings):
        super(PathPrefixResolver, self).__init__(settings)
        locales_re = '|'.join(self.supported_locales)
        self.path_re = re.compile(PATH_PATTERN % locales_re)
        self.prefix_default_locale = getattr(settings,
                'PREFIX_DEFAULT_LOCALE', True)
        self.locale_independent_paths = getattr(settings,
                'LOCALE_INDEPENDENT_PATHS', ())

    def process_request(self, request):
        locale, path = self.split_path(request.path_info)

        # Redirect locale independent paths with locale prefix
        if locale and self.is_locale_independent(path):
            return self.redirection(path, locale)

        # Redirect default locale with prefix unless PREFIX_DEFAULT_LOCALE
        if self.is_default_locale(locale) \
                and not self.prefix_default_locale:
            return self.redirection(path, locale)

        # Redirect paths without prefix if PREFIX_DEFAULT_LOCALE
        if not locale and self.prefix_default_locale \
                and not self.is_locale_independent(path):
            return self.redirection(path, self.get_fallback_locale(request))

        if not locale:
            locale = self.get_fallback_locale(request)
        request.path_info = path
        request.LANGUAGE_CODE = locale

    def redirection(self, path, locale):
        return HttpResponseRedirect(self.build_locale_url(path, locale))

    def split_path(self, path):
        check = self.path_re.match(path)
        if check:
            return check.group('locale'), check.group('path')
        else:
            return '', path

    def is_locale_independent(self, path):
        if django_settings.MEDIA_URL \
                and path.startswith(django_settings.MEDIA_URL):
            return True
        for re in self.locale_independent_paths:
            if re.search(path):
                return True
        return False

    def build_locale_url(self, path, locale=None, request=None):
        if not locale:
            from django.utils import translation
            locale = self.supported_language(translation.get_language())
        if self.is_locale_independent(path):
            pass
        elif self.is_default_locale(locale) \
                and not self.prefix_default_locale:
            pass
        else:
            path = ''.join([u'/', locale, path])
        return ''.join([urlresolvers.get_script_prefix(), path[1:]])

    def parse_locale_url(self, url):
        (_, path) = self.strip_script_prefix(url)
        (locale, path) = self.split_path(path)
        if not locale:
            locale = None
        return (path, locale)

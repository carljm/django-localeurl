# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

import re
from django import http
from django.conf import settings
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.utils import translation
import localeurl
from localeurl.utils import strip_locale_prefix, is_locale_independent, get_language

# Make sure the default language is in the list of supported languages
assert get_language(settings.LANGUAGE_CODE) is not None, \
        "Please ensure that settings.LANGUAGE_CODE is in settings.LANGUAGE."

class LocaleURLMiddleware(object):
    """
    Middleware that sets the language based on the request path prefix and
    strips that prefix from the path. It will also automatically redirect any
    path without a prefix, unless PREFIX_DEFAULT_LOCALE is set to True.
    Exceptions are paths beginning with MEDIA_URL or matching any regular
    expression from LOCALE_INDEPENDENT_PATHS from the project settings.

    For example, the path '/en/admin/' will set request.LANGUAGE_CODE to 'en'
    and request.path to '/admin/'.

    If you use this middleware the django.core.urlresolvers.reverse function
    is be patched to return paths with locale prefix.
    """
    def strip_locale_from_request(self,request):
        check = re.search(r'^/([^/]+)(/.*)$', request.path_info)
        if check is not None:
            locale = check.group(1)
            if get_language(locale) == locale:
                request.path_info = check.group(2)
                return locale
        return None

    def process_request(self, request):
        locale = self.strip_locale_from_request(request)
        if locale is not None:
            if (is_locale_independent(request.path_info)
                    and localeurl.REDIRECT_LOCALE_INDEPENDENT_PATHS):
                return HttpResponseRedirect(request.path_info)
            if (locale == get_language(settings.LANGUAGE_CODE)
                    and not localeurl.PREFIX_DEFAULT_LOCALE):
                return HttpResponseRedirect(request.path_info)
            translation.activate(locale)
            request.LANGUAGE_CODE = translation.get_language()
        elif (not is_locale_independent(request.path)
                and localeurl.PREFIX_DEFAULT_LOCALE):
            return redirect_locale(request)

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response

def redirect_locale(request, path=None, locale=None):
    """
    Prepend a locale to the path. If path is omitted, the request path is used.
    If locale is omitted the current locale is used, or the default from
    settings if the request does not contain LANGUAGE_CODE.
    """
    if path is None:
        path = request.path
    path = strip_locale_prefix(path)
    if locale is None:
        try:
            locale = get_language(request.LANGUAGE_CODE)
        except AttributeError:
            locale = get_language(settings.LANGUAGE_CODE)
    return HttpResponseRedirect('/' + locale + path)

# Replace reverse function
def reverse(viewname, urlconf=None, args=None, kwargs=None):
    """
    Returns the URL from a view name, taking into account locale prefixes.
    """
    path = django_reverse(viewname, urlconf, args, kwargs)
    if is_locale_independent(path):
        return path
    lang = get_language(translation.get_language())
    def_lang = get_language(settings.LANGUAGE_CODE)
    if lang == def_lang and not localeurl.PREFIX_DEFAULT_LOCALE:
        return path
    return '/' + translation.get_language() + path
django_reverse = urlresolvers.reverse
urlresolvers.reverse = reverse

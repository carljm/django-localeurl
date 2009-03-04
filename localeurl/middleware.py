# Copyright (c) 2008-2009 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings
from django.utils import translation
from localeurl.resolver import resolver

class LocaleURLMiddleware(object):
    """
    Middleware that sets the language based on the request URL. The exact
    mapping from URL to locale is defined by the resolver class specified in
    settings.LOCALEURL_RESOLVER.

    If you use this middleware the django.core.urlresolvers.reverse function
    is be patched to return paths with a locale in the URL.
    """
    def __init__(self):
        if not settings.USE_I18N:
            from django.core.exceptions import MiddlewareNotUsed
            raise MiddlewareNotUsed()

    def process_request(self, request):
        response = resolver.process_request(request)
        if response is not None:
            return response
        translation.activate(request.LANGUAGE_CODE)

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response

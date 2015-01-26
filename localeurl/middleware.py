from django.conf import settings
import django.core.exceptions
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils import translation
from django.utils.encoding import iri_to_uri
from django.utils.translation.trans_real import parse_accept_lang_header
from localeurl import settings as localeurl_settings
# Importing models ensures that reverse() is patched soon enough. Refs #5.
from localeurl import models, utils

# Make sure the default language is in the list of supported languages
assert utils.supported_language(settings.LANGUAGE_CODE) is not None, \
        "Please ensure that settings.LANGUAGE_CODE is in settings.LANGUAGES."

class LocaleURLMiddleware(object):
    """
    Middleware that sets the language based on the request path prefix and
    strips that prefix from the path. It will also automatically redirect any
    path without a prefix, unless PREFIX_DEFAULT_LOCALE is set to True.
    Exceptions are paths beginning with MEDIA_URL and/or STATIC_URL (if
    settings.LOCALE_INDEPENDENT_MEDIA_URL and/or
    settings.LOCALE_INDEPENDENT_STATIC_URL are set) or matching any regular
    expression from LOCALE_INDEPENDENT_PATHS from the project settings.

    For example, the path '/en/admin/' will set request.LANGUAGE_CODE to 'en'
    and request.path to '/admin/'.

    Alternatively, the language is set by the first component of the domain
    name. For example, a request on 'fr.example.com' would set the language to
    French.

    If you use this middleware the django.core.urlresolvers.reverse function
    is be patched to return paths with locale prefix (see models.py).
    """
    def __init__(self):
        if not settings.USE_I18N:
            raise django.core.exceptions.MiddlewareNotUsed()

    def process_request(self, request):
        locale, path = utils.strip_path(request.path_info)
        if localeurl_settings.USE_SESSION and not locale:
            slocale = request.session.get('django_language')
            if slocale and utils.supported_language(slocale):
                locale = slocale
        if localeurl_settings.USE_ACCEPT_LANGUAGE and not locale:
            accept_lang_header = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            header_langs = parse_accept_lang_header(accept_lang_header)
            accept_langs = [
                l for l in
                (utils.supported_language(lang[0]) for lang in header_langs)
                if l
            ]
            if accept_langs:
                locale = accept_langs[0]
        locale_path = utils.locale_path(path, locale)
        # locale case might be different in the two paths, that doesn't require
        # a redirect (besides locale they'll be identical anyway)
        if locale_path.lower() != request.path_info.lower():
            locale_url = utils.add_script_prefix(locale_path)

            qs = request.META.get("QUERY_STRING", "")
            if qs:
                # Force this to remain a byte-string by encoding locale_path
                # first to avoid Unicode tainting - downstream will need to
                # handle the job of handling in-the-wild character encodings:
                locale_url = "%s?%s" % (locale_path.encode("utf-8"), qs)

            redirect_class = HttpResponsePermanentRedirect
            if not localeurl_settings.LOCALE_REDIRECT_PERMANENT:
                redirect_class = HttpResponseRedirect
            # @@@ iri_to_uri for Django 1.0; 1.1+ do it in HttpResp...Redirect
            return redirect_class(iri_to_uri(locale_url))
        request.path_info = path
        if not locale:
            try:
                locale = request.LANGUAGE_CODE
            except AttributeError:
                locale = settings.LANGUAGE_CODE
        translation.activate(locale)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response

from django.core import urlresolvers
from django.http import HttpResponseRedirect
from django.utils import translation

class Resolver(object):
    def __init__(self, settings):
        self.settings = settings
        self.supported_locales = dict(settings.LANGUAGES)
        assert self.is_supported_locale(settings.LANGUAGE_CODE), \
                "settings.LANGUAGE_CODE must be in settings.LANGUAGES"

    def process_request(self, request):
        """
        Parses the request URL and sets the LANGUAGE_CODE attribute. The
        default implementation uses the build_locale_url and parse_locale_url
        methods. It may be overridden to be more efficient in extending
        classes.
        """
        url = request.build_absolute_uri()
        path, locale = self.parse_locale_url(url)
        if locale is None:
            locale = self.get_fallback_locale(request)
        locale_url = self.build_locale_url(path, locale, request)
        if url != request.build_absolute_uri(locale_url):
            return HttpResponseRedirect(locale_url)
        request.path_info = path
        request.LANGUAGE_CODE = locale

    def build_locale_url(self, path, locale=None, request=None, prefix=None):
        """
        Returns the URL for the specified path and the locale. If the locale is
        not specified, passing the request is optional (required for the
        'url' tag). This method must be implemented in extending classes.
        """
        raise NotImplementedError

    def parse_locale_url(self, url):
        """
        Returns a tuple (path, locale) from a localized URL (as returned from
        build_locale_url or the patched urlresolvers.reverse function). locale
        is None if no supported locale is found in the URL.
        """
        raise NotImplementedError

    def reverse(self, django_reverse, viewname, urlconf=None, args=[],
            kwargs={}, prefix=None):
        """
        Returns the URL to a view. This function uses the urlresolvers.reverse
        function, strips off the script prefix and call build_locale_url with
        the resulting path. Extending classes may override this method, but
        they do not have to.
        """
        if prefix is None:
            prefix = urlresolvers.get_script_prefix()
        url = django_reverse(viewname, urlconf, args, kwargs, prefix)
        assert url.startswith(prefix)
        return self.build_locale_url(url[len(prefix)-1:])

    def supported_language(self, locale):
        """
        Returns the supported language (from settings.LANGUAGES) for the locale.
        """
        if locale in self.supported_locales:
            return locale
        elif locale[:2] in self.supported_locales:
            return locale[:2]
        else:
            return None

    def get_fallback_locale(self, request=None):
        """
        Returns the default locale. If a language is already set on the request,
        it is used, otherwise settings.LANGUAGE_CODE. The returned locale is
        guaranteed to be in settings.LANGUAGES
        """
        if request is not None and hasattr(request, 'LANGUAGE_CODE'):
            assert self.is_supported_locale(request.LANGUAGE_CODE), \
                    "request.LANGUAGE_CODE must be in settings.LANGUAGES"
            return self.supported_language(request.LANGUAGE_CODE)
        else:
            return self.supported_language(self.settings.LANGUAGE_CODE)

    def is_default_locale(self, locale):
        """
        Returns whether the locale is the default locale.
        """
        return locale == self.supported_language(self.settings.LANGUAGE_CODE)

    def is_supported_locale(self, locale):
        """
        Returns whether the locale is supported, i.e. it is in
        settings.LANGUAGES or its root is.
        """
        return self.supported_language(locale) is not None

    def _default_locale(self):
        """
        The default locale.
        """
        return self.supported_language(self.settings.LANGUAGE_CODE)
    default_locale = property(_default_locale)

    def _current_locale(self):
        """
        The currently activated locale.
        """
        return self.supported_language(translation.get_language())
    current_locale = property(_current_locale)

    def strip_script_prefix(self, url):
        """
        Strips the script prefix from the URL. The function assumes the URL
        starts with the prefix.
        """
        assert url.startswith(urlresolvers.get_script_prefix()), \
                "URL does not start with script prefix: %s" % url
        pos = len(urlresolvers.get_script_prefix()) - 1
        return url[:pos], url[pos:]

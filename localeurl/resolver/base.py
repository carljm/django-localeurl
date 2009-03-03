from django.core import urlresolvers

class Resolver(object):
    def __init__(self, settings, reverse=urlresolvers.reverse):
        self.settings = settings
        self.django_reverse = reverse
        self.supported_locales = dict(settings.LANGUAGES)
        assert self.supported_language(settings.LANGUAGE_CODE) \
                in self.supported_locales, \
                "settings.LANGUAGE_CODE must be in settings.LANGUAGES"

    def process_request(self, request):
        """
        Sets the LANGUAGE_CODE attribute on the request. This method must be
        implemented in extending classes.
        """
        raise NotImplementedError

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

    def reverse(self, viewname, urlconf=None, args=[], kwargs={}, prefix=None):
        """
        Returns the URL to a view. This function uses the urlresolvers.reverse
        function, strips off the script prefix and call build_locale_url with
        the resulting path. Extending classes may override this method, but
        they do not have to.
        """
        if prefix is None:
            prefix = urlresolvers.get_script_prefix()
        url = self.django_reverse(viewname, urlconf, args, kwargs, prefix)
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
            assert self.supported_language(request.LANGUAGE_CODE) \
                    in self.supported_locales, \
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

    def strip_script_prefix(self, url):
        """
        Strips the SCRIPT_PREFIX from the URL. The function assumes the URL
        starts with the prefix.
        """
        assert url.startswith(urlresolvers.get_script_prefix()), \
                "URL does not start with SCRIPT_PREFIX: %s" % url
        pos = len(urlresolvers.get_script_prefix()) - 1
        return url[:pos], url[pos:]

# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

import urlparse
from django.conf import settings as django_settings
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from localeurl.resolver.base import Resolver

class DomainsResolver(Resolver):
    def __init__(self, settings=django_settings):
        super(DomainsResolver, self).__init__(settings)
        self.reverse = self.django_reverse
        self.domains = getattr(settings, 'LOCALEURL_DOMAINS', ())
        self.domain_locale_map = dict(self.domains)
        self.locale_domain_map = dict(map(reversed, self.domains))

        assert all([locale in self.locale_domain_map
                for locale in self.supported_locales]), \
                "settings.LOCALE_DOMAINS must contain all settings.LANGUAGES"
        assert all([locale in self.supported_locales
                for locale in self.locale_domain_map]), \
                "settings.LANGUAGES must contain all settings.LOCALE_DOMAINS"

    def process_request(self, request):
        try:
            locale = self.domain_locale_map[request.get_host()]
        except KeyError:
            # Redirect to the domain for the fallback locale
            return HttpResponseRedirect("%s://%s%s" % (
                    request.is_secure() and 'https' or 'http',
                    self.locale_domain_map[self.get_fallback_locale(request)],
                    request.get_full_path()))
        if not locale:
            locale = self.get_fallback_locale(request)
        request.LANGUAGE_CODE = locale

    def build_locale_url(self, path, locale=None, request=None):
        if locale is None:
            return ''.join([urlresolvers.get_script_prefix(), path[1:]])
        else:
            assert request is not None, \
                    "Request required for building URL with specified locale"
            return "%s://%s%s%s" % (request.is_secure() and 'https' or 'http',
                    self.locale_domain_map[locale],
                    urlresolvers.get_script_prefix(), path[1:])

    def parse_locale_url(self, url):
        (_, domain, path, query, fragment) = urlparse.urlsplit(url)
        if domain:
            try:
                locale = self.domain_locale_map[domain]
            except KeyError:
                locale = None
        else:
            locale = None
        path = urlparse.urlunsplit(('', '', path, query, fragment))
        (_, path) = self.strip_script_prefix(path)
        return (path, locale)

    def get_locale_domain(self, request, locale):
        return "%s://%s" % (request.is_secure() and 'https' or 'http',
                self.locale_domain_map[locale])

# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

import re
from django.conf import settings as django_settings
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from localeurl.resolver.base import Resolver

DOMAIN_PATTERN = r'^(?P<locale>%s)\.(?P<domain>.+)$'

class DomainComponentResolver(Resolver):
    def __init__(self, settings=django_settings):
        super(DomainComponentResolver, self).__init__(settings)
        self.reverse = self.django_reverse
        self.default_locale_component = getattr(settings,
                'DEFAULT_LOCALE_DOMAIN_COMPONENT', self.default_locale)
        locales_re = '|'.join([self.default_locale_component
                if self.is_default_locale(locale) else locale
                for locale in self.supported_locales])
        self.domain_re = re.compile(DOMAIN_PATTERN % locales_re)
        self.domain_reverse = urlresolvers.normalize(DOMAIN_PATTERN)[0][0]

    def process_request(self, request):
        locale, domain = self.split_domain(request.get_host())
        if not self.is_supported_locale(locale):
            # Set locale to fallback language
            locale = self.get_fallback_locale(request)
        request.get_host = lambda: domain
        request.LANGUAGE_CODE = locale

    def build_locale_url(self, path, locale=None, request=None):
        if locale is None:
            return path
        else:
            assert request is not None, \
                    "Request required for building URL with specified locale"
            return "%s://%s%s%s" % (request.is_secure() and 'https' or 'http',
                    self.join_domain(locale, request.get_host()),
                    urlresolvers.get_script_prefix(), path[1:])

    def join_domain(self, locale, domain):
        return self.domain_reverse % {'locale': locale, 'domain': domain}

    def split_domain(self, domain):
        check = self.domain_re.match(domain)
        if check:
            return check.group('locale'), check.group('domain')
        else:
            return '', domain

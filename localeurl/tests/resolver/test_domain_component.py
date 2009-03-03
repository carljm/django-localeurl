import re
from django.test import TestCase
from localeurl.resolver.domain_component import DomainComponentResolver
from localeurl.tests.resolver.test_base import ResolverTestCase
from localeurl.tests.utils import RequestFactory, TestSettings

PATH = '/test/?foo=bar'

class DomainComponentResolverTestCase(ResolverTestCase):
    def get_request(self, domain, request_locale=None):
        request = self.request_factory.get(PATH)
        request.META['SERVER_NAME'] = domain
        if request_locale is not None:
            request.LANGUAGE_CODE = request_locale
        return request

    def process_request(self, domain, request_locale=None):
        request = self.get_request(domain, request_locale)
        resolver = DomainComponentResolver(self.settings)
        response = resolver.process_request(request)
        return request, response

    def _test_sets_language(self, domain, locale, fallback_locale=None):
        request, response = self.process_request(domain, fallback_locale)
        self.assertEqual(None, response)
        self.assertEqual(locale, request.LANGUAGE_CODE)

    def test_sets_language_on_request(self):
        self._test_sets_language('en.example.com', 'en')
        self._test_sets_language('fr.example.com', 'fr')

    def test_sets_fallback_locale_on_unknown_component(self):
        self._test_sets_language('example.com', 'en')
        self._test_sets_language('nl.example.com', 'en')
        self._test_sets_language('example.com', 'fr', fallback_locale='fr')

    def test_uses_default_locale_domain_component(self):
        self.settings['DEFAULT_LOCALE_DOMAIN_COMPONENT'] = 'www'
        self._test_sets_language('www.example.com', 'en')

    def test_build_locale_url(self):
        request = self.get_request('example.com')
        resolver = DomainComponentResolver(self.settings)
        self.assertEqual('http://fr.example.com%s%s' % (self.script_name,
                PATH), resolver.build_locale_url(PATH, 'fr', request))

    def test_parse_locale_url(self):
        resolver = DomainComponentResolver(self.settings)
        path = "%s%s" % (self.script_name, PATH)
        self.assertEqual((PATH, None), resolver.parse_locale_url(path))
        self.assertEqual((PATH, None),
                resolver.parse_locale_url("http://example.com%s" % path))
        self.assertEqual((PATH, None),
                resolver.parse_locale_url("http://nl.example.com%s" % path))
        self.assertEqual((PATH, 'en'),
                resolver.parse_locale_url("http://en.example.com%s" % path))
        self.assertEqual((PATH, 'fr'),
                resolver.parse_locale_url("http://fr.example.com%s" % path))

    def test_reverses_path(self):
        resolver = DomainComponentResolver(self.settings)
        self.assertEqual('%s/test/' % (self.script_name),
                resolver.reverse('localeurl.tests.views.test'))

from django.test import TestCase
from localeurl.resolver.domains import DomainsResolver
from localeurl.tests.resolver.test_base import ResolverTestCase
from localeurl.tests.utils import RequestFactory, TestSettings

PATH = '/test/?foo=bar'

class DomainResolverTestCase(ResolverTestCase):
    def setUp(self):
        super(DomainResolverTestCase, self).setUp()
        self.settings.update(
            LOCALEURL_DOMAINS = (
                ('example.com', 'en'),
                ('example.fr', 'fr'),
            ),
        )

    def get_request(self, domain, request_locale=None):
        request = self.request_factory.get(PATH)
        request.META['SERVER_NAME'] = domain
        if request_locale is not None:
            request.LANGUAGE_CODE = request_locale
        return request

    def process_request(self, domain, request_locale=None):
        request = self.get_request(domain, request_locale)
        response = DomainsResolver(self.settings).process_request(request)
        return request, response

    def _test_sets_language(self, domain, locale):
        request, response = self.process_request(domain)
        self.assertEqual(None, response)
        self.assertEqual(locale, request.LANGUAGE_CODE)

    def _test_redirects(self, domain, redirected_domain, fallback_locale=None):
        request, response = self.process_request(domain, fallback_locale)
        self.assertEqual(302, response.status_code)
        self.assertEqual("http://%s%s%s" % (redirected_domain,
                self.script_name, PATH), response['Location'])

    def test_sets_language_on_request(self):
        self._test_sets_language('example.com', 'en')
        self._test_sets_language('example.fr', 'fr')

    def test_sets_redirects_unknown_domains(self):
        self._test_redirects('example.nl', 'example.com')
        self._test_redirects('example.nl', 'example.fr', fallback_locale='fr')

    def test_build_locale_url(self):
        request = self.get_request('example.com')
        resolver = DomainsResolver(self.settings)
        self.assertEqual('http://example.fr%s%s' % (self.script_name, PATH),
                resolver.build_locale_url(PATH, 'fr', request))

    def test_reverses_path(self):
        resolver = DomainsResolver(self.settings)
        self.assertEqual('%s/test/' % (self.script_name),
                resolver.reverse('localeurl.tests.views.test'))

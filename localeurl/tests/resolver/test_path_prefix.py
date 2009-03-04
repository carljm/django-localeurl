import re
from django.test import TestCase
from django.utils import translation
from localeurl.resolver.path_prefix import PathPrefixResolver
from localeurl.models import django_reverse
from localeurl.tests.resolver.test_base import ResolverTestCase
from localeurl.tests.utils import RequestFactory, TestSettings

class PathPrefixResolverTestCase(ResolverTestCase):
    def setUp(self):
        super(PathPrefixResolverTestCase, self).setUp()
        self.settings.update(
            LOCALE_INDEPENDENT_PATHS = (
                re.compile(r'^/locale_independent/'),
            )
        )

    def process_request(self, path, request_locale=None):
        path = "%s?foo=bar" % path
        request = self.request_factory.get(path)
        if request_locale is not None:
            request.LANGUAGE_CODE = request_locale
        response = PathPrefixResolver(self.settings).process_request(request)
        return request, response

    def _test_sets_language(self, path, locale):
        request, response = self.process_request(path)
        self.assertEqual(None, response)
        self.assertEqual(locale, request.LANGUAGE_CODE)

    def test_sets_language_on_request_if_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = True
        self._test_sets_language('/en/test/', 'en')
        self._test_sets_language('/fr/test/', 'fr')

    def test_sets_language_on_request_if_not_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = False
        self._test_sets_language('/test/', 'en')
        self._test_sets_language('/fr/test/', 'fr')

    def _test_redirects(self, path, redirected_path, fallback_locale=None):
        redirected_path = "%s?foo=bar" % redirected_path
        request, response = self.process_request(path, fallback_locale)
        self.assertEqual(302, response.status_code)
        self.assertEqual("%s%s" % (self.script_name, redirected_path),
                response['Location'])

    def test_redirects_if_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = True
        self._test_redirects('/test/', '/en/test/')
        self._test_redirects('/test/', '/fr/test/', fallback_locale='fr')

    def test_redirects_if_not_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = False
        self._test_redirects('/en/test/', '/test/')

    def test_has_locale_independent_paths(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = True
        self._test_sets_language('/locale_independent/', 'en')

    def test_redirects_li_paths_with_locale_if_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = True
        self._test_redirects('/en/locale_independent/', '/locale_independent/')
        self._test_redirects('/fr/locale_independent/', '/locale_independent/')

    def test_redirects_li_paths_with_locale_if_not_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = False
        self._test_redirects('/en/locale_independent/', '/locale_independent/')
        self._test_redirects('/fr/locale_independent/', '/locale_independent/')

    def test_build_locale_url(self):
        request = self.request_factory.get('/')
        resolver = PathPrefixResolver(self.settings)
        self.assertEqual('%s/fr/test/' % self.script_name,
                resolver.build_locale_url('/test/', 'fr', request))

    def test_parse_locale_url(self):
        resolver = PathPrefixResolver(self.settings)
        path = "/test/?foo=bar"
        self.assertEqual((path, None), resolver.parse_locale_url("%s%s" %
                (self.script_name, path)))
        self.assertEqual((path, 'en'), resolver.parse_locale_url("%s/en%s" %
                (self.script_name, path)))
        self.assertEqual((path, 'fr'), resolver.parse_locale_url("%s/fr%s" %
                (self.script_name, path)))
        self.assertEqual(("/nl%s" % path, None), resolver.parse_locale_url(
                "%s/nl%s" % (self.script_name, path)))

    def _test_reverses_path(self, view, locale, expected_path):
        translation.activate(locale)
        resolver = PathPrefixResolver(self.settings)
        self.assertEqual("%s%s" % (self.script_name, expected_path),
                resolver.reverse(django_reverse, view))

    def test_reverses_path_if_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = True
        self._test_reverses_path('localeurl.tests.views.test', 'en',
                '/en/test/')
        self._test_reverses_path('localeurl.tests.views.test', 'fr',
                '/fr/test/')

    def test_reverses_path_if_not_prefix_default_locale(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = False
        self._test_reverses_path('localeurl.tests.views.test', 'en',
                '/test/')
        self._test_reverses_path('localeurl.tests.views.test', 'fr',
                '/fr/test/')

    def test_reverses_locale_independent_path(self):
        self.settings['PREFIX_DEFAULT_LOCALE'] = True
        self._test_reverses_path('localeurl.tests.views.locale_independent',
                'en', '/locale_independent/')
        self._test_reverses_path('localeurl.tests.views.locale_independent',
                'en', '/locale_independent/')

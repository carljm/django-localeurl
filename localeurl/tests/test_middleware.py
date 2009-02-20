from urlparse import urlparse
from django.core import urlresolvers
from django.conf import settings
from django.test import TestCase
from django.utils import translation
import localeurl.middleware
from localeurl.tests.utils import RequestFactory, TestSettings

LOCALE = 'fr'

class MiddlewareTestCase(TestCase):
    urls = 'localeurl.tests.urls'

    def setUp(self):
        class ResolverStub(object):
            def process_request(self, request):
                request.LANGUAGE_CODE = LOCALE
        self._orig_resolver = localeurl.middleware.resolver
        localeurl.middleware.resolver = ResolverStub()
        self.request = type("RequestStub", (), {})()
        self.middleware = localeurl.middleware.LocaleURLMiddleware()

    def tearDown(self):
        localeurl.middleware.resolver = self._orig_resolver
        translation.deactivate()

    def test_process_request(self):
        self.middleware.process_request(self.request)
        self.assertEquals(LOCALE, translation.get_language())

    def test_process_response(self):
        translation.activate(LOCALE)
        response = {}
        returned_response = self.middleware.process_response(self.request,
                response)
        self.assertEquals(LOCALE, response['Content-Language'])
        self.assertEquals(settings.LANGUAGE_CODE, translation.get_language())
        self.assertEquals(response, returned_response)

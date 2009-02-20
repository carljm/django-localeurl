from urlparse import urlparse
from django.core import urlresolvers
from django.test import TestCase
from django.utils import translation
from localeurl.resolver.domains import DomainsResolver
from localeurl.tests.utils import RequestFactory, TestSettings

class ResolverTestCase(TestCase):
    urls = 'localeurl.tests.urls'

    def setUp(self):
        self.settings = TestSettings(
            LANGUAGES = (
                ('en', "English"),
                ('fr', "French")
            ),
            LANGUAGE_CODE = 'en-us',
        )
        self.script_name = '/script_prefix'
        self.request_factory = RequestFactory(SCRIPT_NAME=self.script_name)
        self._old_script_prefix = urlresolvers.get_script_prefix()
        urlresolvers.set_script_prefix(self.script_name)

    def tearDown(self):
        urlresolvers.set_script_prefix(self._old_script_prefix)
        translation.deactivate()

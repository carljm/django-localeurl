from django import template
from django.template import defaulttags
from django.test import TestCase
from localeurl import resolver
from localeurl.templatetags import localeurl_tags

class TemplateTagsTestCase(TestCase):
    urls = 'localeurl.tests.urls'

    def setUp(self):
        class ResolverStub(object):
            def parse_locale_url(self, url):
                return 'path', 'locale'
            def build_locale_url(self, path, locale, request):
                return '%s_%s_%s' % (path, locale, request)
        self._orig_resolver = resolver.resolver
        resolver.resolver = ResolverStub()
        localeurl_tags.resolver = resolver.resolver

    def tearDown(self):
        resolver.resolver = self._orig_resolver
        localeurl_tags.resolver = self._orig_resolver

    def test_rmlocale(self):
        self.assertEqual('/path', localeurl_tags.rmlocale('/somepath?foo=bar'))

    def test_locale_url_parse(self):
        parser = template.Parser('')
        token = template.Token(template.TOKEN_TEXT,
                'locale_url locale view arg,kwarg=kwval')
        node = localeurl_tags.locale_url(parser, token)
        self.assertEqual('locale', node.locale)
        self.assertEqual('view', node.urlnode.view_name)
        self.assertEqual('arg', node.urlnode.args[0].token)
        self.assertEqual('kwval', node.urlnode.kwargs['kwarg'].token)

    def test_locale_url_as_parse(self):
        parser = template.Parser('')
        token = template.Token(template.TOKEN_TEXT,
                'locale_url locale view arg,kwarg=kwval as asvar')
        node = localeurl_tags.locale_url(parser, token)
        self.assertEqual('locale', node.locale)
        self.assertEqual('view', node.urlnode.view_name)
        self.assertEqual('arg', node.urlnode.args[0].token)
        self.assertEqual('kwval', node.urlnode.kwargs['kwarg'].token)
        self.assertEqual('asvar', node.urlnode.asvar)

    def test_locale_url_render(self):
        urlnode = defaulttags.URLNode('localeurl.tests.views.test',
                [], {}, None)
        node = localeurl_tags.LocaleURLNode('"locale"', urlnode)
        context = template.Context({'request': 'request'})
        self.assertEqual('path_locale_request', node.render(context))

    def test_locale_url_as_render(self):
        urlnode = defaulttags.URLNode('localeurl.tests.views.test',
                [], {}, 'asvar')
        node = localeurl_tags.LocaleURLNode('"locale"', urlnode)
        context = template.Context({'request': 'request'})
        self.assertEqual('', node.render(context))
        self.assertEqual('path_locale_request', context['asvar'])

    def test_locale_url_integration(self):
        context = template.Context({'request': 'request'})
        tmpl = template.Template('{% load localeurl_tags %}'
                '{% locale_url "en" localeurl.tests.views.param_test "hoi" %}')
        self.assertEqual("path_en_request", tmpl.render(context))

    def test_locale_url_as_integration(self):
        context = template.Context({'request': 'request'})
        tmpl = template.Template('{% load localeurl_tags %}'
                '{% locale_url "en" localeurl.tests.views.param_test "hoi"'
                ' as testvar %}{{ testvar}}')
        self.assertEqual("path_en_request", tmpl.render(context))

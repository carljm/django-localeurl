# Copyright (c) 2008 Joost Cassee
# Licensed under the terms of the MIT License (see LICENSE.txt)

from django.conf import settings
from django.core.urlresolvers import get_script_prefix
from django import template
from django.template import Node, Token, TemplateSyntaxError
from django.template import resolve_variable, defaulttags
from django.template.defaultfilters import stringfilter
from django.utils import translation
import localeurl.settings
from localeurl.resolver import resolver

register = template.Library()


def rmlocale(url):
    """Removes the locale prefix from the URL."""
    path, _ = resolver.parse_locale_url(url)
    return ''.join([get_script_prefix(), path])

rmlocale = stringfilter(rmlocale)
register.filter('rmlocale', rmlocale)


def locale_url(parser, token):
    """
    Renders the url for the view with another locale prefix. The syntax is
    like the 'url' tag, only with a locale before the view.

    Examples:
      {% locale_url "de" cal.views.day day %}
      {% locale_url "nl" cal.views.home %}
      {% locale_url "en-gb" cal.views.month month as month_url %}
    """
    bits = token.split_contents()
    if len(bits) < 3:
        raise TemplateSyntaxError("'%s' takes at least two arguments:"
                " the locale and a view" % bits[0])
    urltoken = Token(token.token_type, bits[0] + ' ' + ' '.join(bits[2:]))
    urlnode = defaulttags.url(parser, urltoken)
    return LocaleURLNode(bits[1], urlnode)

class LocaleURLNode(Node):
    def __init__(self, locale, urlnode):
        self.locale = locale
        self.urlnode = urlnode

    def render(self, context):
        locale = resolve_variable(self.locale, context)
        url = self.urlnode.render(context)
        if self.urlnode.asvar:
            self.urlnode.render(context)
            context[self.urlnode.asvar] = chlocale(context[self.urlnode.asvar],
                    locale, context['request'])
            return ''
        else:
            return chlocale(url, locale, context['request'])

register.tag('locale_url', locale_url)

def chlocale(url, locale, request):
    path, _ = resolver.parse_locale_url(url)
    return resolver.build_locale_url(path, locale, request)

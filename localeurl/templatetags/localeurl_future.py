import warnings

warnings.warn(
    "The localeurl_future templatetag library is deprecated; "
    "use localeurl_tags instead.",
    DeprecationWarning
    )

from django import template

from localeurl_tags import locale_url


register = template.Library()


register.tag('locale_url', locale_url)

from django.conf import settings
from django.core import urlresolvers
from django.utils import translation
from localeurl import utils

def reverse(*args, **kwargs):
    reverse_kwargs = kwargs.get('kwargs') or {}
    locale = utils.supported_language(reverse_kwargs.pop(
            'locale', translation.get_language()))
    url = django_reverse(*args, **kwargs)
    _, path = utils.strip_script_prefix(url)
    return utils.locale_url(path, locale)

def resolve(*args, **kwargs):
    locale = utils.supported_language(translation.get_language())
    path = args[0]
    if path.startswith("/%s/" % locale):
        path = path[len("/%s" % locale):]
    return django_resolve(path, *args[1:], **kwargs)

django_resolve = None
django_reverse = None

def patch_reverse():
    """
    Monkey-patches the urlresolvers.reverse function. Will not patch twice.
    """
    global django_reverse
    if urlresolvers.reverse is not reverse:
        django_reverse = urlresolvers.reverse
        urlresolvers.reverse = reverse

def patch_resolve():
    """
    Monkey-patches the urlresolvers.resolve function. Will not patch twice.
    """
    global django_resolve
    if urlresolvers.resolve is not resolve:
        django_resolve = urlresolvers.resolve
        urlresolvers.resolve = resolve

if settings.USE_I18N:
    patch_reverse()
    patch_resolve()
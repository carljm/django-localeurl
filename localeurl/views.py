from urlparse import urlsplit
from django import http
from django.utils.translation import check_for_language
from localeurl import utils
from localeurl import settings as localeurl_settings

def change_locale(request):
    """
    Redirect to a given url while changing the locale in the path
    The url and the locale code need to be specified in the
    request parameters.
    """
    next = request.REQUEST.get('next', None)
    if not next:
        referrer = request.META.get('HTTP_REFERER', None)
        if referrer:
            next = urlsplit(referrer)[2]
    if not next:
        next = '/'
    _, path = utils.strip_path(next)
    if request.method == 'POST':
        locale = request.POST.get('locale', None)
        if locale and check_for_language(locale):
            if localeurl_settings.USE_SESSION:
                request.session['django_language'] = locale
            path = utils.locale_path(path, locale)

    response = http.HttpResponseRedirect(path)
    return response

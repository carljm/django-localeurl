try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from localeurl.views import change_locale

urlpatterns = patterns('',
	url(r'^change/', change_locale, name='localeurl_change_locale'),
)

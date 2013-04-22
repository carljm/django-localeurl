"""
URLconf for testing.
"""
try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('localeurl.tests.test_urls',
     url(r'^dummy/$', 'dummy', name='dummy0'),
     url(r'^dummy/(?P<test>.+)$', 'dummy', name='dummy1'),
)

def dummy(request, test='test'):
    pass

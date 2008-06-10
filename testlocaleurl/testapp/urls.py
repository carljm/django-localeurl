from django.conf.urls.defaults import *

urlpatterns = patterns('django.views.generic.simple',
     (r'^$', 'direct_to_template', {'template': 'test.html'}),
     (r'^independent/', 'direct_to_template', {'template': 'test.html'}),
     (r'^locale_url/$', 'direct_to_template', {'template': 'locale_url.html'}),
     (r'^chlocale/$', 'direct_to_template', {'template': 'chlocale.html'}),
     (r'^rmlocale/$', 'direct_to_template', {'template': 'rmlocale.html'}),
)

urlpatterns += patterns('testapp.views',
     (r'^dummy/(?P<test>.+)$', 'dummy'),
     (r'^dummy/$', 'dummy'),
)

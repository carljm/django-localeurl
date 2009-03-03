from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^test/', 'localeurl.tests.views.test'),
     (r'^param_test/(.*)', 'localeurl.tests.views.param_test'),
     (r'^locale_independent/', 'localeurl.tests.views.locale_independent'),
)

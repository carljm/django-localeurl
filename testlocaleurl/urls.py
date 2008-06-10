from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'^test/', include('testlocaleurl.testapp.urls')),

     #(r'^admin/', include('django.contrib.admin.urls')),
)

from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', direct_to_template,
                    { 'template': 'index.html' }, 'index'),
    (r'^automation/', include('TCC11_12.automation.urls')),
    #(r'^$', 'TCC11_12.automation.views.index'),
    # (r'^TCC/', include('TCC.foo.urls')),
    (r'^contact/', 'TCC11_12.contact.views.contact'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

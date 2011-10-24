
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   (r'^$', 'project.billout.views.bills'),
   (r'^', include('project.billout.urls')),
   url(r'^admin_tools/', include('admin_tools.urls')),
   (r'^admin/', include(admin.site.urls)),
   url(r'login/$', 'django.contrib.auth.views.login', name="login"),
   url(r'logout/$','django.contrib.auth.views.logout', name="logout"),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )


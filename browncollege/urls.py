from django.conf.urls import patterns, include, url, static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('main.urls', namespace='main'), name='home'),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^roster/', include('roster.urls', namespace="roster")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/login/?next=/'},name="logout"),

) + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += staticfiles_urlpatterns()
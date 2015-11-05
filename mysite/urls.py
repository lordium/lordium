from django.conf.urls import patterns, include, url
from django.contrib import admin
import app
from django.conf import settings
from django.conf.urls.static import static

# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'', include('app.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include(app.site.urls)),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# app.autodiscover()
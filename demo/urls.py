from django.conf.urls import include, url
from django.conf import settings
from django.views.static import serve as serve_media

# Uncomment the next two lines to enable the admin:
import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    url(r'^comments/', include('django_comments.urls')),
    url(r'', include(xadmin.site.urls)),
]
if settings.DEBUG:
    urlpatterns += [url(r'^media/(?P<path>.*)$', serve_media, {'document_root': settings.MEDIA_ROOT})]
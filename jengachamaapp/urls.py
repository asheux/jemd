from django.urls import re_path, include
from django.contrib import admin
from jengachamaapp import views
from django.conf import settings
from django.conf.urls.static import static
from contact import views as contact_views
from savings import views as savings_views
from website import views as site_views


admin.autodiscover()


urlpatterns = [
    re_path(r'^$', views.login_redirect, name='login_redirect'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^chamatu/', include('chama.urls', namespace='chamatu')),
    re_path(r'^contact/$', contact_views.contact, name='contact'),
    re_path(r'^savings/', include('savings.urls', namespace='savings')),
    re_path(r'^site/$', site_views.site, name='site'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


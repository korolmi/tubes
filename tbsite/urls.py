from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
  url(r'^$', views.mainPageView, name='mpage'),
  url(r'^listmgr/(?P<listid>[0-9]+)/$', views.listMgrView, name='mgrlist'),
  url(r'^listadd/(?P<listid>[0-9]+)/$', views.listAddView, name='addlist'),
  # url(r'^start/$', views.startView, name='pstart'),
  # url(r'^test/(?P<testid>[0-9]+)/(?P<fid>[0-9]+)/(?P<repstr>[A-Za-z0-9\/\#\-\.]+)/$', views.testRedirView, name='testredir'),
  # url(r'^project/(?P<projid>[0-9]+)/$', views.projView, name='project'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


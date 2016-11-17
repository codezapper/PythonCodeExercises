from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^songs/$', views.index, name='songs'),
    url(r'^albums/$', views.albums, name='albums'),
    url(r'^artists/$', views.artists, name='artists'),
    url(r'^years/$', views.years, name='years'),
    url(r'^detail/([0-9]+)/$', views.detail, name='detail'),
    url(r'^play/([0-9]+)/$', views.play, name='play'),
]

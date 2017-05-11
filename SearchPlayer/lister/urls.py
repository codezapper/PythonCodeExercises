from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^play/([0-9]+)/$', views.play, name='play'),
    url(r'^search/regex/(?P<search_string>.+)$', views.search_regex, name='search'),
    url(r'^search/(?P<search_string>.+)$', views.search, name='search'),
    url(r'^search/$', views.search, name='search'),
]

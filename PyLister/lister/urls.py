from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^albums/$', views.albums, name='albums'),
    url(r'^albums/(?P<album_id>\w+)$', views.albums, name='albums'),
    url(r'^albums/(?P<album_id>\w+)/$', views.albums, name='albums'),
    url(r'^artists/$', views.artists, name='artists'),
    url(r'^artists/(?P<artist_id>\w+)$', views.artists, name='artists'),
    url(r'^artists/(?P<artist_id>\w+)/$', views.artists, name='artists'),
    url(r'^years/$', views.years, name='years'),
    url(r'^years/(?P<year>\w+)$', views.years, name='years'),
    url(r'^years/(?P<year>\w+)/$', views.years, name='years'),
    url(r'^detail/([0-9]+)/$', views.detail, name='detail'),
    url(r'^play/([0-9]+)/$', views.play, name='play'),
    url(r'^search/(?P<search_string>\w+)$', views.search, name='search'),
    url(r'^search/$', views.search, name='search'),
    url(r'^albums_data/([0-9]+)/$', views.albums_data, name='albums_data'),
    url(r'^albums_data/$', views.albums_data, name='albums_data'),
    url(r'^artists_data/([0-9]+)/$', views.artists_data, name='artists_data'),
    url(r'^artists_data/$', views.artists_data, name='artists_data'),
    url(r'^years_data/([0-9]+)/$', views.years_data, name='years_data'),
    url(r'^years_data/$', views.years_data, name='years_data'),
]

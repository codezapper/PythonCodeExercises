from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^songs/$', views.index, name='songs'),
    url(r'^albums/$', views.albums, name='albums'),
    url(r'^artists/$', views.artists, name='artists'),
    url(r'^years/$', views.years, name='years'),
    # ex: /polls/5/details/
    url(r'^detail/([0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/vote/
    url(r'^(?P<song>[0-9]+)/vote/$', views.vote, name='vote'),
]

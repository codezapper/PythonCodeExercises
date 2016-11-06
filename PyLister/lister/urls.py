from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/details/
    url(r'^detail/([0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/vote/
    url(r'^(?P<song>[0-9]+)/vote/$', views.vote, name='vote'),
]

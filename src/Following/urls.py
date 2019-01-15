from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^follower/(?P<followed_id>[0-9]+)/$', views.show_follower, name='follower'),
    url(r'^following/(?P<follower_id>[0-9]+)/$', views.show_following, name='following')
]
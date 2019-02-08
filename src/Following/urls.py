from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'follower/(?P<following_id>[0-9]+)$', views.show_follower, 
    	name='follower'),
    url(r'following/(?P<follower_id>[0-9]+)$', views.show_following, 
    	name='following'),
    url(r'do_follow/(?P<buttonuser_id>[0-9]+)$', views.do_follow, 
    	name='do_follow'),
]
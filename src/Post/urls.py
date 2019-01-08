from django.conf.urls import include, url

from . import views

urlpatterns = [
	url(r'post_list/$', views.all_post_list, name="all_post_list"),
]

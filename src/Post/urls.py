from django.conf.urls import include, url

from . import views

urlpatterns = [
#	url(r'detail/(?P<post_id>[0-9]+)/$', views.post_detail, name="detail"),
#	url(r'user/(?P<post_id>[0-9]+)/$', views.user_post_detail, name="list"),
	url(r'post_list/$', views.all_post_list, name="all_post_list"),
#	url(r'search/', views.post_search, name="search"),
]

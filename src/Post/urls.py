from django.conf.urls import include, url

from . import views

from django.urls import reverse

app_name = 'posts'

urlpatterns = [
	url(r'list/$', views.post_list_view, name="list"),
	url(r'detail/(?P<post_id>\d+)/$', views.post_detail_view, name="detail"),
	url(r'^create/$',views.post_create_view, name ="create"),
	url(r'^edit/(?P<post_id>[0-9]+)/$',views.post_edit_view, name ="edit"),
]

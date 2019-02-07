from django.conf.urls import url, include

from . import views

from django.urls import reverse

app_name = 'posts'

urlpatterns = [
	url(r'^list/$',views.post_list, name = "post_list"),
	url(r'^detail/(?P<post_id>[0-9]+)/$', views.post_detail, name="detail"),
	url(r'^create/$',views.post_create_view, name ="create"),
	url(r'^delete/(?P<post_id>[0-9]+)/$', views.post_delete, name="delete"),
	url(r'^edit/(?P<post_id>[0-9]+)/$',views.post_edit_view, name ="edit"),
	url(r'^user_post_list/(?P<user_id>[0-9]+)/$',views.user_post_list, name ="user_post_list"),	
]

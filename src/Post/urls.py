from django.conf.urls import url, include

from . import views

from django.urls import reverse

urlpatterns = [
<<<<<<< HEAD
	url(r'^list/$',views.post_list_view, name = "post_list"),
	url(r'^detail/(?P<post_id>[0-9]+)/$', views.post_detail_view, name="detail"),
	url(r'^create/$',views.post_create_view, name ="create"),
	url(r'^delete/(?P<post_id>[0-9]+)/$', views.post_delete_view, name="delete"),
	url(r'^edit/(?P<post_id>[0-9]+)/$',views.post_edit_view, name ="edit"),
	url(r'^save_edited/(?P<post_id>[0-9]+)/$',views.post_save_edited_view, name ="save_edited"),
	url(r'^user_post_list/(?P<user_id>[0-9]+)/$',views.user_post_list_view, name ="user_post_list"),
	url(r'^tag_related_post_list/(?P<tag_slug>[0-9a-zA-Z]+)/$',
		views.tag_related_post_list_view, name ="tag_related_post_list"),
	url(r'^author_post_list/(?P<author_slugname>[0-9a-zA-Z]+)/$',views.author_post_list_view, name="author_post_list"),
	
]
=======
	url(r'^user_post_list/$',views.user_post_list_view, name = "user_post_list"),
	url(r'^list/$',views.post_list_view, name = "list"),
	url(r'^detail/(?P<post_id>[0-9]+)/$',views.post_detail_view, name="detail"),
	url(r'^create/$',views.post_create_view, name ="create"),
	url(r'^edit/(?P<post_id>[0-9]+)/$',views.post_edit_view, name="edit"),
	url(r'^delete/(?P<post_id>[0-9]+)/$',views.post_delete_view, name="delete"),
	url(r'^tag_related_post_list/(?P<tag_slug>[0-9a-zA-Z가-힣]+)/$',
		views.tag_related_post_list_view, name ="tag_related_post_list"),
	url(r'^author_post_list/(?P<author_slugname>[0-9a-zA-Z]+)/$'
		,views.author_post_list_view, name="author_post_list"),
	
	]

>>>>>>> 8265418965ca1bb376ed19e13b80cba97650a78f

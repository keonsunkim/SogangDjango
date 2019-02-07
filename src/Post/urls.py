from django.conf.urls import url, include

from . import views

from django.urls import reverse

app_name = 'posts'

urlpatterns = [

	url(r'^list/$',views.post_list_view, name = "list"),
	url(r'^detail/(?P<post_id>[0-9]+)/$',views.post_detail_view, name="detail"),
	url(r'^create/$',views.post_create_view, name ="create"),
	url(r'^edit/(?P<post_id>[0-9]+)/$',views.post_create_view, name="edit"),
	url(r'^user_post_list/$',views.user_post_list_view, name = "user_post_list"),
	url(r'^delete/(?P<post_id>[0-9]+)/$',views.post_delete_view, name="delete"),
	url(r'^tag_related_post_list/(?P<tag_slug>[0-9a-zA-Z]+)/$',
		views.tag_related_post_list_view, name ="tag_related_post_list"),
	url(r'^author_post_list/(?P<author_slugname>[0-9a-zA-Z]+)/$',views.author_post_list_view, name="author_post_list"),
	]


# def i_love_django(name):
# 	print(name) parameter

# i_love_django('yo')

# b = 'lol'
# i_love_django(b)
# argument
# =======
# 	url(r'^list/$',views.post_list, name = "post_list"),
# 	url(r'^detail/(?P<post_id>[0-9]+)/$', views.post_detail, name="detail"),
# 	url(r'^create/$',views.post_create_view, name ="create"),
# 	url(r'^delete/(?P<post_id>[0-9]+)/$', views.post_delete, name="delete"),
# 	url(r'^edit/(?P<post_id>[0-9]+)/$',views.post_edit_view, name ="edit"),
# 	url(r'^user_post_list/(?P<user_id>[0-9]+)/$',views.user_post_list, name ="user_post_list"),	
# ]
# >>>>>>> ff5d8967f7ff061dd7eed60404fc0e2c36354b28

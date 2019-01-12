from django.conf.urls import include, urls
from . import views

urlpatterns = [
    url(r'detail/(?P<post_id>[0-9]+)/$',views.post_detail, name='detail'),
    url(r'user/(?P<user_id>[0-9]+)/$',views.user_post_list, name='user_post_list'),
    url(r'search/',views.post_search, name='search'),
 ]
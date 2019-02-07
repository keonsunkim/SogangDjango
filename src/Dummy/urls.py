from django.conf.urls import url

from .views import dummy_base_view, dummy_home_view

urlpatterns = [
    url(r'base$', dummy_base_view, name='base'),
    url(r'home$', dummy_home_view, name='home'),
]

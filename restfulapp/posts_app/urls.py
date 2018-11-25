from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^(?P<pk>\d*)/like', PostViewSet.as_view({'get': 'like_post'}), name='like_post'),
    re_path(r'^(?P<pk>\d*)/', PostViewSet.as_view({'get': 'get_post'}), name='get_post'),
    re_path(r'^$', PostViewSet.as_view({'get': 'get_post_list'}))
]
"""restfulapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework_jwt.views import obtain_jwt_token

from accounts_app import views as acc_view
from posts_app import views as posts_view

#It better might be router
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^create_user/', acc_view.CreateUserViewSet.as_view({'post': 'create'}), name='create_user'),
    re_path(r'^authenticate/$', obtain_jwt_token),
    re_path(r'^posts/create_post/$', posts_view.PostViewSet.as_view({'post': 'create'}), name='create_post'),
    path('posts/', include('posts_app.urls'))
]

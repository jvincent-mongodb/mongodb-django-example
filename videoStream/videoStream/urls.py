"""
URL configuration for videoStream project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from videoStreamApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', views.index, name="index"),
    path('api/user/<str:username>', views.user_detail, name="user_detail"),
    path('api/user/create/', views.user, name="create_user"),
    path('api/upload/video/', views.upload_video, name="upload_video"),
    path('api/stream/video/<str:filename>', views.stream_video, name="stream_video"),
]


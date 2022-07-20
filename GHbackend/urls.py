"""GHbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.db.models import base
from django.urls import path 
from django.conf.urls import include 
from rest_framework.routers import DefaultRouter
from espsensor import views

router = DefaultRouter()
router.register(r'GH' , views.GreenViewSet)


urlpatterns = [
    path("api/sensor/<int:nodename>",views.api_sensor , name = "給感測器傳值使用"),
    path("api/now/<int:nodename>/<int:esp>" , views.api_now , name = "現在某個特定esp 資料"),
    path("api/history/<int:nodename>/<int:esp>" , views.api_history , name = "過去某個特定esp 資料"),
    path("api/history/<int:nodename>/<int:esp>/<int:datestart>/<int:dateend>" , views.api_history , name = "過去某區間esp資料"),
    path('admin/', admin.site.urls),
    # path('api/' , include(router.urls)),
]
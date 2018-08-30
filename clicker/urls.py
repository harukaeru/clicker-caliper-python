"""clicker URL Configuration

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
from django.urls import path
from django.conf.urls import include, url
from clickercore.views import (
    index, launch, new, clicker_create, clicker_show, clicker_answer,
    clicker_start, clicker_stop
)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'clicker', index, name='main-view'),
    path(r'clicker/new', new),
    path(r'clicker/create', clicker_create, name='clicker-create'),
    url(r'clicker/(?P<clickerItemId>\d+)/answer', clicker_answer, name='clicker-answer'),
    url(r'clicker/(?P<clickerItemId>\d+)/start', clicker_start, name='clicker-start'),
    url(r'clicker/(?P<clickerItemId>\d+)/stop', clicker_stop, name='clicker-stop'),
    url(r'clicker/(?P<clickerItemId>\d+)', clicker_show, name='clicker-show'),
    path(r'launch', launch, name='launch-view'),
]

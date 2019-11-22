"""auto_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import url
from autoservice import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, ),
    url(r'^register/', views.register ),
    url(r'^cars/', views.cars ),
    url(r'^change_user_data/', views.change_user_data ),
    url(r'^change_lang/', views.change_lang ),
    url(r'^add_car/', views.user_add_car ),
    url(r'^user_detail/', views.user_detail ),
    url(r'^login/', views.logon ),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include('autoservice.api_urls')),
]

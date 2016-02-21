"""clockin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import moge_web.views

urlpatterns = [
    url(r'^$', moge_web.views.index),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/', moge_web.views.logout),
    url(r'^login/', moge_web.views.login),
    url(r'^register/', moge_web.views.register),
    url(r'^display/(?P<list_id>[0-9]+)', moge_web.views.display),
    url(r'^display', moge_web.views.display),
]

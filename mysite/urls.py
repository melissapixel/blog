"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.views.decorators.cache import cache_page

sitemaps = {
    'posts': PostSitemap,
}

# Вставляем шаблоны адресов в главный шаблон
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')), # Все URL-адреса из файла blog/urls.py будут доступны под префиксом /blog/

    # единая точка для всех sitemaps
    path('sitemap.xml', cache_page(3600)(sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

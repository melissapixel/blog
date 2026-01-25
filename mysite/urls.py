from django.contrib import admin
from django.urls import path, include

from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.views.decorators.cache import cache_page

from django.views.generic import TemplateView, RedirectView


sitemaps = {
    'posts': PostSitemap,
}

# Вставляем шаблоны адресов в главный шаблон
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
    path('', RedirectView.as_view(pattern_name='blog:post_list')),


    # Static Pages
    path('about/', 
        TemplateView.as_view(
            template_name='static/about.html',
            extra_context={'title': 'About'}
        ), name='about'),

    path('contact/', 
        TemplateView.as_view(
            template_name='static/contact.html',
            extra_context={'title': 'Contact'}
        ), name='contact'),


    # единая точка для всех sitemaps
    path('sitemap.xml', cache_page(3600)(sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

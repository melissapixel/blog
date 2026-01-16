from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    limit = 10000                       # ← максимум записей в одном файле
    changefreq = 'weekly'               # Как часто поисковики должны проверять обновления этой страницы
    priority = 0.9                      # важность страницы по шкале от 0.0 до 1.0.

    def items(self):                    # Какие объекты включить в карту сайта.
         return Post.published.all()
    
    def lastmod(self, obj):             # Когда страница была последний раз изменена.
        return obj.updated
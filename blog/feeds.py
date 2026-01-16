from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy    # используется для того, чтобы генерировать URL-адрес для атрибута link.
from .models import Post
import markdown

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):                            # Какие посты включить
        return Post.published.all()[:5]
    
    def item_title(self, item):                 # Как отобразить заголовок одного поста
        return item.title
    
    def item_description(self, item):           # Как отобразить описание (анонс) поста
        return truncatewords_html(markdown.markdown(item.body), 30)
    
    def item_pubdate(self, item):               # агрегаторы используют эту дату, чтобы определить, новый ли это пост
        return item.publish
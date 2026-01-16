from django import template
from ..models import Post
from django.db.models import Count
# from django.utils import timezone
# from datetime import timedelta


register = template.Library()

# счетчик количества всех опубликованных постов
@register.simple_tag
def total_posts():
    return Post.published.count()

# показ названий последних опубликованных постов
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


# показ постов, у которых самое большее количество комментариев
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


# @register.simple_tag
# def time_ago(datetime_obj):
#     now = timezone.now()
#     diff = now - datetime_obj
#     if diff < timedelta(minutes=1):
#         return "только что"
#     elif diff < timedelta(hours=1):
#         minutes = int(diff.total_seconds() // 60)
#         return f"{minutes} мин. назад"
#     elif diff < timedelta(days=1):
#         hours = int(diff.total_seconds() // 3600)
#         return f"{hours} ч. назад"
#     else:
#         return datetime_obj.strftime("%d %b %Y")
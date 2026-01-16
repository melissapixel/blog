from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]
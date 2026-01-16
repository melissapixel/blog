from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.simple_tag
def time_ago(datetime_obj):
    now = timezone.now()
    diff = now - datetime_obj
    if diff < timedelta(minutes=1):
        return "только что"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() // 60)
        return f"{minutes} мин. назад"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() // 3600)
        return f"{hours} ч. назад"
    else:
        return datetime_obj.strftime("%d %b %Y")
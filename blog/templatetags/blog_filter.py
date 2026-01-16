from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library() 

# для преобразования пользовательского контента - в красивый
@register.filter(name='markdown')   # имя фильтра в шаблоне
def markdown_format(text):
    return mark_safe(markdown.markdown(text))  # Markdown-текст в HTML
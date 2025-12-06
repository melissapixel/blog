from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()

    publish = models.DateTimeField(default=timezone.now) # Когда пост опубликован (можно настроить)
    created = models.DateTimeField(auto_now_add=True) # Когда пост создан (нельзя изменить
    updated = models.DateTimeField(auto_now=True) # при обновлении меняется дата

    # определим зараннее порядок выдачи постов
    class Meta:
        # указываем атрибут, и правила сортировки
        ordering = ['-publish']
        # указываем опцию-индексс, дабы сортировка была быстрее
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
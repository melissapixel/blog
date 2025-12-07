from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # чтобы работать с пользователями

# Create your models here.
class Post(models.Model):

    # даем выбор тексстовых значений
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    # добавляем модель в поле нашей модели
    author = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='blog_posts')

    publish = models.DateTimeField(default=timezone.now) # Когда пост опубликован (можно настроить)
    created = models.DateTimeField(auto_now_add=True) # Когда пост создан (нельзя изменить
    updated = models.DateTimeField(auto_now=True) # при обновлении меняется дата

    # поле, свзанное с классом статуса
    status = models.CharField(max_length=2,
        choices=Status.choices, # ← берём варианты из Status
        default=Status.DRAFT)   # ← значение по умолчанию
    
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
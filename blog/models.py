from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # чтобы работать с пользователями
from django.urls import reverse # формирует URL-адрес динамически

# создаем свой менеджер, который смотрит только опубликованные посты
class PublishedManager(models.Manager):
    def get_queryset(self): # ядро менеджера.
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)
    
# Create your models here.
class Post(models.Model):

    # поля модели
    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной (наш) менеджер

    # даем выбор тексстовых значений
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish') # поле slug уникально для поля даты
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
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                    args=[self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug])
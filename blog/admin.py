from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# добавляем удобство
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] # показываем нужные поля в списке
    list_filter = ['status', 'created', 'publish'] # атрибут фильтров
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)} # автоматический путь
    raw_id_fields = ['author'] # делаем поиск по автору, а не ищем по списку
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

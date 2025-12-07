from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)

# добавляем удобство
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status'] # показываем нужные поля в списке
    list_filter = ['status', 'created', 'publish'] # атрибут фильтров
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)} # автоматический путь
    raw_id_fields = ['author'] # делаем поиск по автору, а не ищем по списку
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


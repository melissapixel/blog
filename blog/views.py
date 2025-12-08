from django.shortcuts import render
from .models import Post

# Create your views here.
def post_list(request): # для этого представления используем 1 обьект. Этот обьект необходим для всех функций-представлений
    posts = Post.published.all() # используем менеджер
    return render(request,
        'blog/post/list.html', # путь к шаблону
        {'posts': posts}) # контекстные переменные

from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_list(request): # для этого представления используем 1 обьект. Этот обьект необходим для всех функций-представлений
    posts = Post.published.all() # используем менеджер
    return render(request,
        'blog/post/list.html', # путь к шаблону
        {'posts': posts}) # контекстные переменные


# создаем представление о подробности поста
def post_detail(request, year, month, day, post):
    # используем функцию исключения
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request,
        'blog/post/detail.html',
        {'post': post})
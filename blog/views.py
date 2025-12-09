from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator

# Create your views here.

def post_list(request):
    # получаем все опубликованные посты
    posts = Post.published.all() # используем менеджер

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1) # извлекаем HTTP GET-параметр page. При отсуствии - значение 1.
    posts = paginator.page(page_number) # получаем обьект с методами

    return render(request,
        'blog/post/list.html', # путь к шаблону
        {'posts': posts}) # подсставляем контекст


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
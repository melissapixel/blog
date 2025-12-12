from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm # выгружаем нашу форму
from django.core.mail import send_mail # функция, которая отправляет email через SMTP-сервер
from django.views.decorators.http import require_POST # декоратор.

# Create your views here.

def post_list(request):
    # получаем все опубликованные посты
    posts = Post.published.all() # используем менеджер

    # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1) # извлекаем HTTP GET-параметр page. При отсуствии - значение 1.
    try:
        posts = paginator.page(page_number) # получаем обьект с методами
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # Если page_number не число, то
        # выдать первую страницу результатов
        posts = paginator.page(1)
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
    comments = post.comments.filter(active=True)    # Список активных комментариев к посту
    form = CommentForm()                            # Форма для комментирования пользователями
    return render(request,
        'blog/post/detail.html',
        {'post': post,
         'comments': comments,
         'form': form})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                            id=post_id,
                            status=Post.Status.PUBLISHED)
    sent = False # флаг: письмо не отправлено

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST) # создаем эксземпляр формы EmailPostForm, заполняя её данными из запроса (request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data  # сохраняем сюда данные

            #   получаем ссылку, чтобы отправить по емейл
            post_url = request.build_absolute_uri( # например: http://127.0.0.1:8000/blog/5/
                post.get_absolute_url())   # например: /blog/5/.
            
            # example: Алиса recommends you read Как настроить Django
            subject = f"{cd['name']} recommends you read " \
                f"{post.title}"
            
            # Формирует тело письма
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['name']}\'s comments: {cd['comments']}"
            
            # Отправляет email через SMTP:
            send_mail(subject, message, 'newazzzno@gmail.com',
                [cd['to']])
            
            # флаг, что письмо отпралено
            sent = True
    else:
        form = EmailPostForm()  # создаем пустую форму
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,   # либо пустая, либо с данными
                                                    'sent': sent})  #  флаг: было ли письмо отправлено.


@require_POST # «надеваем» декоратор на функцию
# представление, чтобы управлять передачей поста на обработку
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                            id=post_id,
                            status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)   # request.POST — содержит данные, отправленные через форму. Мы передаём их в CommentForm → форма заполняется этими данными.
    if form.is_valid():
        comment = form.save(commit=False) # создай объект Comment в памяти, но не записывай в БД
        comment.post = post # Назначить пост комментарию
        comment.save()      # Сохранить комментарий в базе данных
    return render(request, 'blog/post/comment.html',    # мы всегда возвращаем один и тот же шаблон
                            {'post': post,
                            'form': form,
                            'comment': comment})
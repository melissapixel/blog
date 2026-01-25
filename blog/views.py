from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.contrib.postgres.search import TrigramSimilarity
from .forms import EmailPostForm, CommentForm,  SearchForm # выгружаем нашу форму
from django.core.mail import send_mail # функция, которая отправляет email через SMTP-сервер
from django.views.decorators.http import require_POST # декоратор.
from taggit.models import Tag
from django.db.models import Count
from django.views.generic import ListView


class PostList(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    tag = None
    queryset = Post.published.all()
    context_object_name = 'posts'
    ordering = ["-publish"]
    paginate_orphans = 1
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        queryset = Post.published.all()                                 # Начинаем с опубликованных постов
        tag_slug = self.kwargs.get('tag_slug')                          # Получаем tag_slug из URL (если есть)

        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)            # Находим тег или 404
            queryset = queryset.filter(tags__in=[self.tag])             # Фильтруем посты по тегу
        else:
            self.tag = None
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag                                       # передаём tag в шаблон
        return context


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

    # Получаем ID тегов текущего поста
    post_tags_ids = post.tags.values_list('id', flat=True)

    # Находим другие посты, у которых есть хотя бы один общий тег
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                .exclude(id=post.id)\
                                .annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags')[:4]
    
    return render(request,
        'blog/post/detail.html',
        {'post': post,
         'comments': comments,
         'form': form,
         'similar_posts': similar_posts})


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


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.1).order_by('-similarity')

    # ← ВЫНОСИМ render() ЗА ПРЕДЕЛЫ УСЛОВИЯ!
    return render(request,
        'blog/post/search.html',
        {'form': form,
         'query': query,
         'results': results})
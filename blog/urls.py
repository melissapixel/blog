from django.urls import path # функция маршрутов
from . import views # все предсставления
from .views import PostList
from .feeds import LatestPostsFeed

app_name = 'blog' # именное пространство приложения, дабы потом ссылаться на него

# когда пользователь заходит на какой-то url, то вызови его представление
urlpatterns = [
    # представления поста
    path('', 
         PostList.as_view(), 
         name='post_list'),  # → /blog/

    path('tag/<slug:tag_slug>/',
            PostList.as_view(),
            name='post_list_by_tag'),
    
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
        views.post_detail, 
        name='post_detail'), # →  /blog/2022/1/1/who-was-django-reinhardt/

    path('post/<int:post_id>/share/', 
         views.post_share, 
         name='post_share'), # /blog/post/5/share/
    
    path('<int:post_id>/comment/', 
         views.post_comment, 
         name='post_comment'), # /blog/post/5/comment/

     path('feed/', LatestPostsFeed(), name='post_feed'),
     path('search/', views.post_search, name='post_search'),
]
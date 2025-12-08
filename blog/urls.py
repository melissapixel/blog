from django.urls import path # функция маршрутов
from . import views # все предсставления

app_name = 'blog' # именное пространство приложения, дабы потом ссылаться на него

# когда пользователь заходит на какой-то url, то вызови его представление
urlpatterns = [
    # представления поста
    path('', views.post_list, name='post_list'),  # → /blog/
    path('<int:id>/', views.post_detail, name='post_detail'), # → /blog/5/
]
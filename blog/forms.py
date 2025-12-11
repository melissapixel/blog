# Определение формы
from django import forms

from .models import Comment

# новый класс наследуется от forms.Form (не привязан к модели)
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()                      # проверяет, похоже ли на емейл
    to = forms.EmailField()
    comments = forms.CharField(required=False,      # необязательно для заполнения
                            widget=forms.Textarea)  # указывает, как отображать поле
    

class CommentForm(forms.ModelForm):                 # форма Django, привязанная к модели.
    class Meta:                                     # инструкция для Django, что делать
        model = Comment                             # форма работает с моделью Comment
        fields = ['name', 'email', 'body']          # Из всех полей модели покажи в форме ТОЛЬКО эти три
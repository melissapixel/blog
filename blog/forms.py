# Определение формы
from django import forms

# новый класс наследуется от forms.Form (не привязан к модели)
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField() # автоматически проверяет, похоже ли на емейл
    to = forms.EmailField()
    comments = forms.CharField(required=False, # необязательно для заполнения
                            widget=forms.Textarea) # указывает, как отображать поле
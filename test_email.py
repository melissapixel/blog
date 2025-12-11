# test_email.py
import os
import sys
import django

# Указываем, где находятся настройки Django
# ЗАМЕНИ 'mysite' на имя своей папки с settings.py!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Настраиваем Django
django.setup()

# Теперь можно использовать любые компоненты Django
from django.core.mail import send_mail

if __name__ == '__main__':
    try:
        result = send_mail(
            subject="Тестовое письмо из Django",
            message="Если вы читаете это — всё работает!",
            from_email="newazzzno@gmail.com",          # ← твой Gmail
            recipient_list=["newazzzno@gmail.com"],    # ← список получателей
            fail_silently=False
        )
        print(f"✅ Письмо отправлено! Количество отправленных: {result}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
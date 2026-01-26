import string
from django.test import TestCase
from core.utils import generate_url_id

class GenerateUrlIdTest(TestCase):
    def test_generate_url_id_returns_string(self):
        """Функция должна возвращать строку."""
        result = generate_url_id()
        self.assertIsInstance(result, str)

    def test_generate_url_id_default_length(self):
        """По умолчанию длина — 8 символов."""
        result = generate_url_id()
        self.assertEqual(len(result), 8)

    def test_generate_url_id_custom_length(self):
        """Можно задать свою длину."""
        result = generate_url_id(12)
        self.assertEqual(len(result), 12)

    def test_generate_url_id_contains_only_allowed_chars(self):
        """ID должен содержать только буквы и цифры (без спецсимволов)."""
        result = generate_url_id(20)
        allowed_chars = set(string.ascii_letters + string.digits)
        self.assertTrue(set(result).issubset(allowed_chars))

    def test_generate_url_id_is_random(self):
        """Последовательные вызовы дают разные значения."""
        id1 = generate_url_id()
        id2 = generate_url_id()
        self.assertNotEqual(id1, id2)  # маловероятно, но возможно совпадение → допустимо в тесте
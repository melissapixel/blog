import secrets
import string

def generate_url_id(length: int = 8) -> str:
    """
    Генерирует короткий, URL-safe, криптографически безопасный ID.
    
    Состоит из букв (a-z, A-Z) и цифр (0-9).
    Пример: 'aB3x9KmQ'
    
    Args:
        length: длина идентификатора (по умолчанию 8)
    
    Returns:
        str: уникальный ID
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
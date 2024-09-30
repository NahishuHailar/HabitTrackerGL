import pytest
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def user(db):
    """
    Фикстура для создания тестового пользователя с email и паролем.
    """
    return User.objects.create(
        email='testuser@example.com',
        password='password123',
        firebase_key='firebase123',
        auth_type='none',
        color='green'
    )

@pytest.fixture
def token(user):
    """
    Фикстура для генерации JWT-токена для тестового пользователя.
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
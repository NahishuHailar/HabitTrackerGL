import pytest
from django.contrib.auth import get_user_model
from django.http import HttpRequest
from users.auth.email_auth_backend import EmailAuthBackend

@pytest.fixture
def user(db):
    # Создаем тестового пользователя
    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )
    return user

@pytest.mark.django_db
def test_authenticate_success(user):
    """
    Тест успешной аутентификации
    """
    backend = EmailAuthBackend()

    request = HttpRequest()
    authenticated_user = backend.authenticate(request, username="testuser@example.com", password="password123")

    assert authenticated_user is not None
    assert authenticated_user.email == user.email

@pytest.mark.django_db
def test_authenticate_wrong_password(user):
    """
    Тест на неправильный пароль
    """
    backend = EmailAuthBackend()

    request = HttpRequest()
    authenticated_user = backend.authenticate(request, username="testuser@example.com", password="wrongpassword")

    assert authenticated_user is None

@pytest.mark.django_db
def test_authenticate_non_existent_user():
    """
    Тест на несуществующего пользователя
    """
    backend = EmailAuthBackend()

    request = HttpRequest()
    authenticated_user = backend.authenticate(request, username="nonexistent@example.com", password="password123")

    assert authenticated_user is None



@pytest.mark.django_db
def test_get_user_success(user):
    """
    Тест успешного получения пользователя по его ID
    """
    backend = EmailAuthBackend()

    fetched_user = backend.get_user(user.id)
    assert fetched_user is not None
    assert fetched_user.email == user.email

@pytest.mark.django_db
def test_get_user_non_existent():
    """
    Тест получения несуществующего пользователя
    """
    backend = EmailAuthBackend()

    fetched_user = backend.get_user(999) 
    assert fetched_user is None

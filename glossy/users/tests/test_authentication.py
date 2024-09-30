import pytest
from unittest import mock
from django.http import HttpRequest
from users.auth.authentication import FirebaseAuthentication
from users.models import User
from users.auth.exceptions import NoAuthToken, InvalidAuthToken

@pytest.fixture
def firebase_auth_mock():
    with mock.patch("users.auth.authentication.auth.verify_id_token") as mock_verify_id_token:
        yield mock_verify_id_token

@pytest.mark.django_db
def test_no_auth_token():
    """
    Тест на отсутствие заголовка авторизации, который должен выбросить NoAuthToken.
    """
    auth_instance = FirebaseAuthentication()
    request = HttpRequest()

    with pytest.raises(NoAuthToken):
        auth_instance.authenticate(request)


@pytest.mark.django_db
def test_invalid_auth_token(firebase_auth_mock):
    """
    Тест на недействительный токен, который должен выбросить InvalidAuthToken.
    """
    auth_instance = FirebaseAuthentication()
    request = HttpRequest()
    request.META["HTTP_AUTHORIZATION"] = "Bearer invalid_token"

    firebase_auth_mock.side_effect = Exception("Invalid token")

    with pytest.raises(InvalidAuthToken):
        auth_instance.authenticate(request)


@pytest.mark.django_db
def test_successful_authentication(firebase_auth_mock):
    """
    Тест на успешную аутентификацию с корректным токеном и созданием пользователя.
    """
    auth_instance = FirebaseAuthentication()
    request = HttpRequest()
    request.META["HTTP_AUTHORIZATION"] = "Bearer valid_token"
    request.META["HTTP_FCMTOKEN"] = "fcm_token_123"

    decoded_token = {
        "uid": "firebase_user_123",
        "email": "testuser@example.com",
        "name": "Test User",
    }

    firebase_auth_mock.return_value = decoded_token

    user, _ = auth_instance.authenticate(request)

    assert user.firebase_key == "firebase_user_123"
    assert user.email == "testuser@example.com"
    assert user.username == "Test User"
    assert user.fcm_key == "fcm_token_123"


@pytest.mark.django_db
def test_update_existing_user(firebase_auth_mock):
    """
    Тест на успешное обновление существующего пользователя с новым FCM ключом.
    """
    # Создаем пользователя заранее
    existing_user = User.objects.create(
        firebase_key="firebase_user_123",
        email="testuser@example.com",
        username="Test User",
        fcm_key="old_fcm_token"
    )

    auth_instance = FirebaseAuthentication()
    request = HttpRequest()
    request.META["HTTP_AUTHORIZATION"] = "Bearer valid_token"
    request.META["HTTP_FCMTOKEN"] = "new_fcm_token"

    decoded_token = {
        "uid": "firebase_user_123",
        "email": "testuser@example.com",
        "name": "Test User",
    }

    firebase_auth_mock.return_value = decoded_token

    user, _ = auth_instance.authenticate(request)

    assert user == existing_user
    assert user.fcm_key == "new_fcm_token"  # Проверяем, что FCM ключ обновился

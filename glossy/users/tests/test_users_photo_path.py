import pytest
from users.models import User
from users.services.users_photo_path import user_directory_path


@pytest.mark.django_db
def test_user_directory_path():
    # Создаем тестового пользователя
    user = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )

    # Проверяем путь с дефолтным именем файла
    expected_path = f"users/{user.id}/profile_photo/profile"
    assert user_directory_path(user) == expected_path

    # Проверяем путь с кастомным именем файла
    custom_filename = "custom_image.jpg"
    expected_path_custom = f"users/{user.id}/profile_photo/{custom_filename}"
    assert user_directory_path(user, custom_filename) == expected_path_custom

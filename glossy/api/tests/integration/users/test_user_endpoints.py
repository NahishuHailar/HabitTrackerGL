import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestUserEndpoints:

    @pytest.fixture(autouse=True)
    def setup(self, user, token):
        """
        Автоматически вызывается перед каждым тестом.
        Устанавливаем клиента и URL для получения текущего пользователя.
        """
        self.client = APIClient()
        self.user_url = reverse('get_user')  # Эндпоинт для получения текущего пользователя
        self.user = user
        self.token = token

    def test_get_user_unauthorized(self):
        """
        Тестируем, что доступ без токена возвращает 401 Unauthorized.
        """
        response = self.client.get(self.user_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_get_user_authorized(self):
    #     """
    #     Тестируем успешный запрос с токеном авторизованного пользователя.
    #     """
    #     # Устанавливаем токен в заголовок авторизации
    #     self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    #     # Выполняем запрос
    #     response = self.client.get(self.user_url)

    #     # Проверяем статус и данные
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data['id'] == str(self.user.id)
    #     assert response.data['email'] == self.user.email
    #     assert response.data['firebase_key'] == self.user.firebase_key

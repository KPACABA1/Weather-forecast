from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock


class WeatherViewTest(TestCase):
    def setUp(self):
        """Общие данные для всех тестов"""
        self.city = 'Moscow'
        self.url = reverse('weather:get_weather')
        self.api_key = 'fake_api_key_123'
        self.weather_data = {
            "name": "Moscow",
            "sys": {"country": "RU"},
            "main": {
                "temp": 25,
                "feels_like": 20,
                "humidity": 47,
                "pressure": 1013
            },
            "weather": [{
                "description": "небольшая облачность",
                "icon": "04d"
            }],
            "wind": {"speed": 6}
        }


    @patch('weather.views.requests.get')
    def test_get_weather_success(self, mock_get):
        """Тест на успешный запрос c использованием мока"""
        # Настраиваем мок
        mock_response = Mock()
        mock_response.json.return_value = self.weather_data
        mock_get.return_value = mock_response

        # Подменяем API-ключ в окружении
        with patch.dict('os.environ', {'OPENWEATHERMAP_API_KEY': self.api_key}):
            # Делаем POST-запрос к view
            response = self.client.post(self.url, data={'city': self.city},
                                        content_type='application/x-www-form-urlencoded')

        # Проверяем, что API вызвалось с правильным URL
        expected_url = f"http://api.openweathermap.org/data/2.5/weather?q=&appid={self.api_key}&units=metric&lang=ru"
        mock_get.assert_called_once_with(expected_url)

        # Проверяем ответ view
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moscow")  # Город в HTML
        self.assertContains(response, "25°C")  # Температура
        self.assertContains(response, "небольшая облачность")  # Описание
import requests
from django.shortcuts import render

import os
from dotenv import load_dotenv

load_dotenv()


def weather(request):
    # Готовим данные
    weather_data = None
    error = None
    city = ''

    if request.method == 'POST':
        # Получаем название города
        city = request.POST.get('city', '')

        try:
            # Получаем API ключ из настроек и делаем запрос к сервису openweathermap
            api_key = os.getenv('OPENWEATHERMAP_API_KEY')
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

            response = requests.get(url)
            # Проверяем на ошибки
            response.raise_for_status()
            if response:
                data = response.json()
                # Форматируем данные для шаблона
                weather_data = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temp': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'description': data['weather'][0]['description'],
                    'icon': data['weather'][0]['icon'],
                    'humidity': data['main']['humidity'],
                    'pressure': round(data['main']['pressure'] * 0.750064),
                    'wind': round(data['wind']['speed']),
                }

        # Если город не найден, сообщаем об этом пользователю
        except requests.exceptions.RequestException as e:
            error = f"Ошибка при запросе к API: {str(e)}"

    return render(request, 'weather.html', {
        'weather_data': weather_data,
        'error': error,
        'city': city,
    })

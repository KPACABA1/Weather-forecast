import requests
from django.http import JsonResponse
from django.shortcuts import render

import os
from dotenv import load_dotenv

from weather.models import UserCityHistory

load_dotenv()


api_key = os.getenv('OPENWEATHERMAP_API_KEY')


def weather(request):
    # Готовим данные
    weather_data = None
    error = None
    city = ''
    recent_cities = []

    if request.method == 'POST':
        # Получаем название города
        city = request.POST.get('city', '')

        try:
            # Получаем API ключ из настроек и делаем запрос к сервису openweathermap
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

                # Функционал при котором при поиске города, дополнительно создавалась история поиска
                history, created = UserCityHistory.objects.get_or_create(user=request.user, city=city)

                if not created:
                    history.search_count += 1
                    history.save()

        # Если город не найден, сообщаем об этом пользователю
        except requests.exceptions.RequestException as e:
            error = f"Ошибка при запросе к API: {str(e)}"

        # Получаем последние 3 города для авторизованных пользователей
        if request.user.is_authenticated:
            recent_cities = UserCityHistory.objects.filter(user=request.user).order_by('-last_search')[:3]

    return render(request, 'weather.html', {
        'weather_data': weather_data,
        'error': error,
        'city': city,
        'recent_cities': recent_cities,
    })


def city_autocomplete(request):
    """Вьюшка для создания подсказок при наборе города в вьюшке weather"""
    # Делаем настройки для создания подсказок
    query = request.GET.get('term', '')
    if not query:
        # Пустой список, если запрос пустой
        return JsonResponse([], safe=False)

    # Делаем запрос
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={api_key}"
    try:
        response = requests.get(url)
        # Проверяем что ответ успешный или вызывается ошибка
        response.raise_for_status()
        # Потом принтануть и узнать какой ответ даёт
        cities = response.json()

        # Форматируем ответ
        suggestions = [
            {"label": f"{city['name']}, {city.get('country', '')}", "value": city["name"]} for city in cities
        ]
        return JsonResponse(suggestions, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse([], safe=False)

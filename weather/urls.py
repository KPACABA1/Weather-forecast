from django.urls import path
from weather.apps import WeatherConfig
from weather.views import weather, city_autocomplete

app_name = WeatherConfig.name

urlpatterns = [
    path('', weather, name='get_weather'),
    path('city-autocomplete/', city_autocomplete, name='city_autocomplete')
]

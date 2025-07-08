from django.urls import path
from weather.apps import WeatherConfig
from weather.views import weather

app_name = WeatherConfig.name

urlpatterns = [
    path('', weather, name='get_weather'),
]

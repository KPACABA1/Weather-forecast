from django.urls import path, include
from weather.apps import WeatherConfig
from weather.views import weather

app_name = WeatherConfig.name

urlpatterns = [
    path('', weather, name='weather'),
]

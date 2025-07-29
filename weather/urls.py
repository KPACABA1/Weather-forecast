from django.urls import path
from weather.apps import WeatherConfig
from weather.views import weather, city_autocomplete, CityListAPIView

app_name = WeatherConfig.name

urlpatterns = [
    path('', weather, name='get_weather'),
    path('city-autocomplete/', city_autocomplete, name='city-autocomplete'),
    path('city-history/', CityListAPIView.as_view(), name='city-history'),
]

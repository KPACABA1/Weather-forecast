from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Урлы для приложения погоды
    path('', include('weather.urls', namespace='weather')),
    path('users/', include('users.urls', namespace='users')),
]

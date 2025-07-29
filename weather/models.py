from django.db import models

from users.models import User


class UserCityHistory(models.Model):
    """Модель для отслеживания последних городов пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    city = models.CharField(max_length=20, verbose_name='Город который искал пользователь')
    search_count = models.PositiveIntegerField(default=1, verbose_name='Сколько раз искали город')
    last_search = models.DateTimeField(auto_now=True, verbose_name='Последняя дата поиска города')

    class Meta:
        # чтобы не было дублей
        unique_together = ('user', 'city')
        # сортировка по дате
        ordering = ['-last_search']

    def __str__(self):
        return f"{self.user}: {self.city} ({self.search_count})"

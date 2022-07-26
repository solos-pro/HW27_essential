from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Координата"
        verbose_name_plural = "Координаты"


class User(models.Model):
    ROLES = [
        ("member", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Админ")
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, null=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=9, choices=ROLES, default="member")
    age = models.PositiveSmallIntegerField(null=True)
    locations = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]


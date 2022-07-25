# from django.contrib.auth.models import User
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Advertisement(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    # author = models.CharField(max_length=20)
    price = models.PositiveSmallIntegerField(null=False)
    description = models.CharField(max_length=1000, default="None")
    address = models.CharField(max_length=1000)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="advertisements/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"




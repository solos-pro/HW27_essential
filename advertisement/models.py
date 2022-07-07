from django.db import models


class Advertisement(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=200)
    price = models.PositiveSmallIntegerField(null=False)
    description = models.CharField(max_length=1000, default="None")
    address = models.CharField(max_length=1000)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


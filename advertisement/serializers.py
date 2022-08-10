from rest_framework import serializers

from advertisement.models import Advertisement, Category
from users.models import Location
from users.serializers import LocationsSerializer, UsersSerializer


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdvertisementsSerializer(serializers.ModelSerializer):
    location = LocationsSerializer(read_only=True)
    category = CategoriesSerializer(read_only=True)
    author = UsersSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = '__all__'
        # fields = ['name', 'author', 'price', 'description', 'category', 'location']


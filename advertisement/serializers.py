from rest_framework import serializers

from advertisement.models import Advertisement, Category
from users.models import Location
from users.serializers import LocationsSerializer


class AdvertisementsSerializer(serializers.ModelSerializer):
    location = LocationsSerializer(
        read_only=True,
        # many=True,
    )

    class Meta:
        model = Advertisement
        # fields = '__all__'
        fields = ['price', 'name', 'author', 'location']


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
from rest_framework import serializers

from users.models import Location, User


class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    locations = LocationsSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'locations']


class UserSerializer(serializers.ModelSerializer):
    locations = LocationsSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    locations = LocationsSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user

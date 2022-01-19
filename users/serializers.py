from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data.get('username'),
                                        password=validated_data.get('password'))
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'last_request_time')

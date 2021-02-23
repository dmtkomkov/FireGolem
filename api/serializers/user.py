from django.contrib.auth.models import User
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from api.models import UserIcon


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ShortUserSerializer(ModelSerializer):
    user_icon = SlugRelatedField(read_only=True, slug_field='icon')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_icon')


class UserIconSerializer(ModelSerializer):
    class Meta:
        model = UserIcon
        fields = ('icon',)
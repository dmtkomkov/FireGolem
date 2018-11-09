from rest_framework.serializers import ModelSerializer, SlugRelatedField

from django.contrib.auth.models import User
from api.models import Post, UserIcon


class UserIconSerializer(ModelSerializer):
    class Meta:
        model = UserIcon
        fields = ('icon',)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ShortUserSerializer(ModelSerializer):
    user_icon = SlugRelatedField(read_only = True, slug_field = 'icon')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_icon')

class PostSerializer(ModelSerializer):
    user = ShortUserSerializer(read_only = True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'created', 'user')

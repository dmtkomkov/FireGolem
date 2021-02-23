from rest_framework.serializers import ModelSerializer

from api.models import Post
from api.serializers.user import ShortUserSerializer


class PostSerializer(ModelSerializer):
    user = ShortUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'created', 'user')

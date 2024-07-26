from rest_framework.serializers import ModelSerializer
from .models import Music
from rest_framework import serializers

class MusicSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format="%m/%d %H:%M", read_only=True)
    created_at2 = serializers.DateTimeField(format="%m/%d", read_only=True)
    username = serializers.CharField(read_only=True)
    profile = serializers.URLField(read_only=True)
    writer = serializers.PrimaryKeyRelatedField(read_only=True)
    nickname = serializers.CharField(read_only=True)

    class Meta:
        model = Music
        fields = [ 'id', 'title', 'author', 'content', 'image', 'writer', 'created_at', 'created_at2', 'username', 'profile', 'nickname']
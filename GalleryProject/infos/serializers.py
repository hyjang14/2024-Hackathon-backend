from rest_framework.serializers import ModelSerializer
from .models import Info
from rest_framework import serializers

class InfoSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format="%d/%m/%y %H:%M", read_only=True)
    username = serializers.CharField(read_only=True)
    profile = serializers.URLField(read_only=True)
    writer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Info
        fields = [ 'id', 'title', 'author', 'content', 'image', 'writer', 'created_at', 'username', 'profile']
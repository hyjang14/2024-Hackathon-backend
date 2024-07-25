from rest_framework.serializers import ModelSerializer
from .models import Book
from rest_framework import serializers

class BookSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format="%y/%m/%d %H:%M", read_only=True)
    username = serializers.CharField(read_only=True)
    profile = serializers.URLField(read_only=True)
    writer = serializers.PrimaryKeyRelatedField(read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Book
        fields = [ 'id', 'title', 'author', 'content', 'image', 'writer', 'created_at', 'username', 'profile']

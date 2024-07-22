from rest_framework.serializers import ModelSerializer
from .models import Post, Analysis, Like
from rest_framework import serializers

class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [ 'id', 'title', 'content', 'img', 'writer', 'view_at', 'created_at', 'like_count']

    def validate_title(self, value):
        if len(value) > 15:
            raise serializers.ValidationError("제목은 15글자를 초과할 수 없습니다.")
        return value
    
    def get_like_count(self, obj):
        return obj.like_count()

class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
    

class AnalysisSerializer(ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Analysis
        fields = ['id', 'post', 'analysis', 'happiness', 'sadness', 'anger', 'anxiety', 'created_at']
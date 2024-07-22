from rest_framework import serializers
from .models import DataModel, Scrap, Comment

# openApi
class DataSerializer(serializers.ModelSerializer):
        class Meta:
            model = DataModel
            fields = ['id', 'title', 'description', 'image', 'pageUrl', 'author', 'period', 'time', 'place', 'contact', 'audience', 'scrap_count']


        def get_scrap_count(self, obj):
            return obj.scrap_count()

# 스크랩
class ScrapSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    data = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Scrap
        fields = ['id', 'user', 'data', 'created_at']

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    data = serializers.PrimaryKeyRelatedField(queryset=DataModel.objects.all())
    created_at = serializers.DateTimeField(format="%m/%d", read_only=True)
    username = serializers.CharField(read_only=True)
    profile = serializers.URLField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    data = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'data', 'comment', 'created_at', 'username', 'profile']
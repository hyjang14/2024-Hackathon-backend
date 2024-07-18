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
    class Meta:
        model = Scrap
        fields = ['id', 'user', 'data', 'created_at']

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    data = serializers.PrimaryKeyRelatedField(queryset=DataModel.objects.all())
    class Meta:
        model = Comment
        fields = ['id', 'user', 'data', 'comment', 'created_at']
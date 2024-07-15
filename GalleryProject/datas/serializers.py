from rest_framework import serializers
from .models import DataModel, Scrap

# openApi
class DataSerializer(serializers.ModelSerializer):
        class Meta:
            model = DataModel
            fields = ['id', 'title', 'description', 'image', 'pageUrl', 'author', 'period', 'time', 'place', 'contact', 'audience']

# 스크랩
class ScrapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scrap
        fields = ['id', 'user', 'data', 'created_at']
from rest_framework import serializers
from .models import DataModel, Scrap, Comment, Rating
from django.db.models import Avg, Count

# openApi
class DataSerializer(serializers.ModelSerializer):
        average_rating = serializers.SerializerMethodField()
        rating_count = serializers.SerializerMethodField()

        class Meta:
            model = DataModel
            fields = ['id', 'title', 'description', 'image', 'pageUrl', 'author', 'period', 'time', 'place', 'contact', 'audience', 'scrap_count', 'average_rating', 'rating_count']

        def get_scrap_count(self, obj):
            return obj.scrap_count()
        
        def get_average_rating(self, obj):
            average = obj.ratings.aggregate(Avg('score'))['score__avg']

            if average is None:
                return 0.0  # 기본값 0.0
            return round(average, 1)  # 소수점 첫째자리까지만

        def get_rating_count(self, obj):
            return obj.ratings.aggregate(Count('id'))['id__count'] or 0 


# 스크랩
class ScrapSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    data = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    image = serializers.URLField(read_only=True)
    period = serializers.CharField(read_only=True)
    place = serializers.CharField(read_only=True)
    
    class Meta:
        model = Scrap
        fields = ['id', 'user', 'data', 'created_at', 'is_scrapped', 'title', 'image', 'period', 'place']

# 댓글
class CommentSerializer(serializers.ModelSerializer):
    data = serializers.PrimaryKeyRelatedField(queryset=DataModel.objects.all())
    created_at = serializers.DateTimeField(format="%m/%d", read_only=True)
    username = serializers.CharField(read_only=True)
    profile = serializers.URLField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    data = serializers.PrimaryKeyRelatedField(read_only=True)
    nickname = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'data', 'comment', 'created_at', 'username', 'profile', 'nickname']

# 별점
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
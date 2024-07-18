from rest_framework.serializers import ModelSerializer
from .models import Info

class InfoSerializer(ModelSerializer):
    class Meta:
        model = Info
        fields = [ 'id', 'title', 'author', 'content', 'image', 'writer', 'created_at']
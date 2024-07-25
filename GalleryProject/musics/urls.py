from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import MusicViewSet

music_router = SimpleRouter(trailing_slash=True)
music_router.register('musics', MusicViewSet, basename='music')

urlpatterns = [
    path('', include(music_router.urls)),
]
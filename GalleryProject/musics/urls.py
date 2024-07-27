from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import MusicViewSet

music_router = SimpleRouter(trailing_slash=True)
music_router.register('musics', MusicViewSet, basename='music')

urlpatterns = [
    path('datas/<int:exhibition_id>/', include(music_router.urls)),
]
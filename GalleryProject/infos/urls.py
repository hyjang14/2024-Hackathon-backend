from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import InfoViewSet

info_router = SimpleRouter(trailing_slash=True)
info_router.register('infos', InfoViewSet, basename='info')

urlpatterns = [
    path('', include(info_router.urls)),
]
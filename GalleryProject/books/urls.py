from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import BookViewSet

book_router = SimpleRouter(trailing_slash=True)
book_router.register('books', BookViewSet, basename='book')

urlpatterns = [
    path('datas/<int:exhibition_id>/', include(book_router.urls)),
]
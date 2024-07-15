from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from .views import UserUpdateView, ProfileView

user_router = SimpleRouter()
user_router.register('user',views.UserViewSet)

urlpatterns = [
    # 회원가입
    path('',include(user_router.urls)),

    # 회원정보 조회
    path('user/<int:pk>/', ProfileView.as_view()),

    # 회원정보 수정
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),

    # drf 인증 패키지(로그인: rest-auth/login)
    path('auth/', include('rest_framework.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
]
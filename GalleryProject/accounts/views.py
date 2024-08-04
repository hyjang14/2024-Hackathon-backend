from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, ProfileSerializer, CustomLoginSerializer
from rest_framework import viewsets, generics, status
from .permissions import CustomReadOnly
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import serializers

from dj_rest_auth.views import LoginView

from musics.models import Music
from books.models import Book
from posts.models import Post
from datas.models import DataModel, Comment
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

# 로그인

class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    @csrf_exempt
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        print(f"Serializer is valid: {serializer.is_valid()}")
        print(f"Validated data: {serializer.validated_data}")
        
        # 응답 데이터 반환
        return Response({
            'token': serializer.validated_data['token'],
            'usercode': serializer.validated_data['usercode']
        }, status=status.HTTP_200_OK)

# 로그아웃
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()  # 현재 사용자 토큰 삭제
        return Response(status=status.HTTP_204_NO_CONTENT)

# 회원가입
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 회원정보 수정
class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user
    
    def perform_update(self, serializer):
        user = self.get_object()
        new_nickname = serializer.validated_data['nickname']
        # new_profile_image = serializer.validated_data['profile']

        super().perform_update(serializer)

        
        # 사용자가 작성한 모든 글의 닉네임을 업데이트
        Music.objects.filter(writer=user).update(nickname=new_nickname)
        Book.objects.filter(writer=user).update(nickname=new_nickname)
        Post.objects.filter(writer=user).update(nickname=new_nickname)
        Comment.objects.filter(user=user).update(nickname=new_nickname)

        # if new_profile_image:
        profile_image_url = user.profile.url
        Music.objects.filter(writer=user).update(profile=profile_image_url)
        Book.objects.filter(writer=user).update(profile=profile_image_url)
        Post.objects.filter(writer=user).update(profile=profile_image_url)
        Comment.objects.filter(user=user).update(profile=profile_image_url)

    
# 회원정보 조회
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly]
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, ProfileSerializer, CustomLoginSerializer
from rest_framework import viewsets, generics, status
from .permissions import CustomReadOnly
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework import serializers

from dj_rest_auth.views import LoginView

# 로그인
class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        print(f"Serializer is valid: {serializer.is_valid()}")
        print(f"Validated data: {serializer.validated_data}")
        
        # 응답 데이터 반환
        return Response({
            'token': serializer.validated_data.get('token'),
            'usercode': serializer.validated_data.get('usercode')
        }, status=status.HTTP_200_OK)


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
    
# 회원정보 조회
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomReadOnly]
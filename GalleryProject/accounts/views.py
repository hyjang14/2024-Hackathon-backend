from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, ProfileSerializer
from rest_framework import viewsets, generics, permissions
from .permissions import CustomReadOnly
from rest_framework.permissions import AllowAny

# 회원가입
class UserViewSet(viewsets.ModelViewSet):
    # 인증없어도 누구나 할 수 있도록 함
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
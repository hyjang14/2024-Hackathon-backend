from .models import Info
from .serializers import InfoSerializer
from rest_framework.viewsets import ModelViewSet 

from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly  # 커스텀 권한 클래스 임포트

class InfoViewSet(ModelViewSet): 
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    # 자신이 쓴 글만 수정/삭제할 수 있도록
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(writer = self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(writer = self.request.user)

    def perform_destroy(self, instance):
        instance.delete()

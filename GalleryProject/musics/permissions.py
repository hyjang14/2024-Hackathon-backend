from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 사용자에게 허용하므로 SAFE_METHODS (GET, HEAD, OPTIONS) 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 쓰기 권한은 댓글 작성자에게만 허용
        return obj.writer == request.user
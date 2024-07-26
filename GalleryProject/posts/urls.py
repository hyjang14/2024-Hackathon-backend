from rest_framework.routers import SimpleRouter
from django.urls import path, include
from .views import PostViewSet, MyPostViewSet, AnalyzePostView, AnalysisListView, LikeCreateView, LikeView, PostLikeListView, LikeDeleteView

post_router = SimpleRouter(trailing_slash=True)
post_router.register('posts', PostViewSet, basename='post')

myPost_router = SimpleRouter(trailing_slash=True)
myPost_router.register('myposts', MyPostViewSet, basename='myposts')

# analysis_router = SimpleRouter(trailing_slash=False)
# analysis_router.register('analyze-post', AnalyzePostView.as_view(), basename='analyze-post')

urlpatterns = [
    # 기록글
    path('', include(post_router.urls)),
    path('', include(myPost_router.urls)),

    # 분석
    path('analyze-post/<int:pk>/', AnalyzePostView.as_view(), name='analyze-post'),
    path('analysis-results/', AnalysisListView.as_view(), name='analysis-results'),

    # 좋아요 생성
    path('likes/<int:post_id>/', LikeCreateView.as_view(), name='like-create'),
    # 좋아요 전체조회
    path('likes/all/', LikeView.as_view(), name='like-view'),
    # 특정 기록글의 좋아요 조회
    path('likes/<int:post_id>/', PostLikeListView.as_view(), name='Post-like-view'),
    # 좋아요 삭제
    path('likes/<int:post_id>/delete/', LikeDeleteView.as_view(), name='like-delete'),

]
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import DataViewSet, Dataload, ScrapCreateView, ScrapDeleteView, ScrapView, ExhibitionScrapListView


data_router = SimpleRouter()
data_router.register('data', DataViewSet)

urlpatterns = [
    # 데이터베이스를 초기화하거나 갱신할때만 사용
    path('load-data/', Dataload, name='load-data'), 

    # 전시 전체조회
    path('', include(data_router.urls)),
    
    # 스크랩 생성
    path('scraps/', ScrapCreateView.as_view(), name='scrap-create'),
    # 스크랩 전체조회
    path('scraps/all/', ScrapView.as_view(), name='scrap-view'),
    # 특정 전시회의 스크랩 조회
    path('scraps/<int:exhibition_id>/', ExhibitionScrapListView.as_view(), name='exhibition-scrap-view'),
    # 스크랩 삭제
    path('scraps/<int:exhibition_id>/delete/', ScrapDeleteView.as_view(), name='scrap-delete'),
]
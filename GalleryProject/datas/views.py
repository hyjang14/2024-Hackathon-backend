from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import DataModel, Scrap # model
from .serializers import DataSerializer, ScrapSerializer # serializer

# 스크랩
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# 공공 API
import time
import requests # 외부 API 요청을 위한 requests 모듈
from django.http import HttpResponse # HTTP 응답을 위한 클래스
import xml.etree.ElementTree as ET
import json

from rest_framework.permissions import AllowAny


class DataViewSet(ModelViewSet):
    # 인증없어도 누구나 할 수 있도록 함
    permission_classes = [AllowAny]

    pagination_class = None  # 페이지네이션 사용 안 함

    queryset = DataModel.objects.all().order_by('id') # 모든 객체를 ID 순으로 정렬하여 쿼리셋으로 설정
    serializer_class = DataSerializer # Serializers를 사용하여 데이터 직렬화


def Dataload(request):
    time.sleep(3)  # 1초간의 지연을 추가합니다.
    # 외부 API에 요청을 보냄
    response = requests.get(
        'http://api.kcisa.kr/openapi/API_CCA_149/request?serviceKey=6348160e-80d1-430f-9e84-f8d5d0ff206e'
    )
    print(response.text)
    root = ET.fromstring(response.text)

    # 필요한 데이터 추출
    items = root.find('.//items')
    
    item_list = []
    for item in items.findall('item'):
        item_dict = {
            'TITLE': item.find('TITLE').text,
            'DESCRIPTION': item.find('DESCRIPTION').text,
            'IMAGE_OBJECT': item.find('IMAGE_OBJECT').text,
            'URL': item.find('URL').text,
            'AUTHOR': item.find('AUTHOR').text,
            'PERIOD': item.find('PERIOD').text,
            'EVENT_PERIOD': item.find('EVENT_PERIOD').text,
            'CNTC_INSTT_NM': item.find('CNTC_INSTT_NM').text,
            'CONTACT_POINT': item.find('CONTACT_POINT').text,
            'AUDIENCE': item.find('AUDIENCE').text,
        }
        item_list.append(item_dict)

    # JSON으로 변환
    json_data = json.dumps(item_list)

    # 가져온 데이터를 데이터베이스에 저장
    for item in item_list:
        try:
            # 이미 존재하는 data 객체가 있는지 확인
            existing_data = DataModel.objects.get(title=item['TITLE'])
            continue # 존재하면 다음 루프로 넘어감

        except:
            # 존재하지 않으면 새로운 Character 객체를 생성하고 저장
            DataModel(
                title=item.get('TITLE', ''),
                description=item.get('DESCRIPTION', ''),
                image=item.get('IMAGE_OBJECT', ''),
                pageUrl=item.get('URL', ''),
                author=item.get('AUTHOR', ''),
                period=item.get('PERIOD', ''),
                time=item.get('EVENT_PERIOD', ''),
                place=item.get('CNTC_INSTT_NM', ''),
                contact=item.get('CONTACT_POINT', ''),
                audience=item.get('AUDIENCE', ''),
            ).save()


    return HttpResponse(json_data)


# 스크랩 생성
class ScrapCreateView(generics.CreateAPIView):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 스크랩 전체조회
class ScrapView(generics.ListAPIView):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer


# 특정전시 스크랩 조회
class ExhibitionScrapListView(generics.ListAPIView):
    serializer_class = ScrapSerializer

    def get_queryset(self):
        exhibition_id = self.kwargs['exhibition_id']
        return Scrap.objects.filter(data=exhibition_id)  # 전시회 ID에 해당하는 스크랩
    

# 스크랩 삭제
class ScrapDeleteView(generics.DestroyAPIView):
    queryset = Scrap.objects.all()
    serializer_class = ScrapSerializer

    def get_object(self):
        exhibition_id = self.kwargs['exhibition_id']
        try:
            # exhibition_id와 매칭되는 Scrap 객체를 가져옵니다.
            obj = self.queryset.get(data__id=exhibition_id, user=self.request.user)
            self.check_object_permissions(self.request, obj)  # 객체 권한 검사
            return obj
        except Scrap.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
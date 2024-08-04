from .models import Post, Analysis, Like
from .serializers import PostSerializer, AnalysisSerializer, LikeSerializer
from rest_framework.viewsets import ModelViewSet 
from rest_framework.generics import ListAPIView
from datas.models import DataModel
from datas.serializers import DataSerializer
import re

from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly  # 커스텀 권한 클래스 임포트

# 좋아요
from rest_framework import generics
from django.http import Http404

# AI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from django.conf import settings

# 기록글 검색
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# 기록글 전체보기
class PostViewSet(ModelViewSet): 
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    # 자신이 쓴 글만 수정/삭제할 수 있도록
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # 후기글 검색 
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('title', 'content') # 후기글 제목으로 검색할 수 있게 함

    def perform_create(self, serializer):
        serializer.save(writer = self.request.user)


# 내 기록글만 보기
class MyPostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(writer=self.request.user)


# 좋아요 생성
class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')

        try:
            post_instance = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            self.kwargs['post_id'] = None  
            return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        like, created = Like.objects.get_or_create(user=self.request.user, post=post_instance)

        # 좋아요 상태를 토글합니다.
        like.toggle_like()

        # 새로운 좋아요이 생성되었거나 기존 좋아요의 상태가 변경된 것을 저장합니다.
        serializer.instance = like

        serializer.save(user=self.request.user, post=post_instance)



# 좋아요 전체조회
class LikeView(generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer



# 특정 기록 좋아요 조회
class PostLikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post=post_id)  # 전시회 ID에 해당하는 스크랩
    

# 좋아요 삭제
class LikeDeleteView(generics.DestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_object(self):
        post_id = self.kwargs['post_id']
        try:
            # post_id와 매칭되는 Like 객체를 가져옵니다.
            obj = self.queryset.get(post_id=post_id, user=self.request.user)
            self.check_object_permissions(self.request, obj)  # 객체 권한 검사
            return obj
        except Like.DoesNotExist:
            raise Http404

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AnalysisListView(ListAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Analysis.objects.filter(post__writer=user).order_by('-created_at')


# AI 감정분석
openai.api_key = settings.OPENAI_API_KEY

class AnalyzePostView(APIView): 
    def get(self, request, pk):
        try: 
            post = Post.objects.get(pk=pk) 
        except Post.DoesNotExist: 
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND) 
        model = "gpt-3.5-turbo" 
        
        # 프롬프트 
        query = (
            "이 글을 정말 자세하게 심리 분석하고 설명해주세요. 감정이 아닌 심리분석이기 때문에 오직 심리분석만 하세요."
            "그 다음 무조건 심리 분석 결과에 따라 꼭 [행복: , 슬픔: , 분노: , 불안: ]이 형식으로 4가지의 퍼센트를 도출해주세요. 다른 감정은 필요없고 4가지 감정은 꼭 포함되어야합니다. 심리분석에 나타나지 않은 감정은 0%라고 분석해도 괜찮습니다. 이때 각 퍼센트는 합해서 무조건 100%가 되어야 합니다."
            "감정에 따라서 아래의 전시회 데이터 중 적절한 전시회를 추천해주세요. 추천 이유와 함께 추천해주세요."
            "필수로 이 세가지 형식을 맞춰서 해주세요."
        )

        # 전시회 데이터를 가져오기
        exhibitions = DataModel.objects.all()
        exhibition_summaries = self.summarize_exhibitions(exhibitions)
        # exhibition_data = "\n".join([f"{exhibition.title}: {exhibition.description}" for exhibition in exhibitions])

        # 메시지 설정하기
        messages = [ {"role": "system", "content": "You are a helpful assistant"},
                     {"role": "user", "content": post.content},
                     {"role": "user", "content": query},
                     {"role": "user", "content": exhibition_summaries} ] 
        
        try: 

            # API 호출 
            response = openai.ChatCompletion.create( 
                 model=model, 
                 messages=messages ) 
                #  temperature=0.8 ) 
            

            # 응답 출력 
            answer = response['choices'][0]['message']['content'] 
            
            emotions = self.parse_emotions(answer)

            happiness = emotions.get('행복', 0) 
            sadness = emotions.get('슬픔', 0) 
            anger = emotions.get('분노', 0) 
            anxiety = emotions.get('불안', 0) 
            
            # 분석 결과 저장 
            analysis_result = Analysis.objects.create( 
                 post=post, 
                 analysis=answer, 
                 happiness=happiness, 
                 sadness=sadness, 
                 anger=anger, 
                 anxiety=anxiety ) 
            
            return Response({ 'post': PostSerializer(post).data, 'analysis_result': AnalysisSerializer(analysis_result).data }, status=status.HTTP_200_OK)
        except openai.error.OpenAIError as e: # OpenAI API 오류 처리 
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
    def parse_emotions(self, text): # 감정 퍼센트를 추출하기 위한 정규식 
        pattern = re.compile(r'행복\s*:\s*(\d+)%|슬픔\s*:\s*(\d+)%|분노\s*:\s*(\d+)%|불안\s*:\s*(\d+)%') 
        emotions = {'행복': 0, '슬픔': 0, '분노': 0, '불안': 0} 
        matches = pattern.findall(text) 
            
        for match in matches: 
            if match[0]: emotions['행복'] = float(match[0]) 
            if match[1]: emotions['슬픔'] = float(match[1]) 
            if match[2]: emotions['분노'] = float(match[2]) 
            if match[3]: emotions['불안'] = float(match[3]) 
                
        return emotions
    
    def summarize_exhibitions(self, exhibitions):  # 추가된 부분
        summaries = []
        for exhibition in exhibitions:
            summary = f"{exhibition.title}: {exhibition.description[:50]}..."  # 전시회 설명의 처음 50자만 사용
            summaries.append(summary)
        return "\n".join(summaries)
    
    def parse_recommendations(self, text, exhibitions):
        # 전시회 추천 결과를 파싱하기 위한 로직
        recommended_titles = re.findall(r'Recommended Exhibition: (.+)', text)
        recommended_exhibitions = exhibitions.filter(title__in=recommended_titles)
        return recommended_exhibitions
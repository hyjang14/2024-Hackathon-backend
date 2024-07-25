from .models import Post, Analysis, Like
from .serializers import PostSerializer, AnalysisSerializer, LikeSerializer
from rest_framework.viewsets import ModelViewSet 
from rest_framework.generics import ListAPIView
import re

# 좋아요
from rest_framework import generics
from django.http import Http404

# AI
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from django.conf import settings

class PostViewSet(ModelViewSet): 
    queryset = Post.objects.all().order_by('-created_at') 
    # queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer = self.request.user)



# 좋아요 생성
class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer


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
        query = "이 글을 심리 분석하고 행복, 슬픔, 분노, 불안의 퍼센트를 도출해주세요. 각 퍼센트는 합해서 100%가 되어야 합니다. 감정 퍼센트를 마지막에 정리해서 알려주세요." 
        
        # 메시지 설정하기
        messages = [ {"role": "system", "content": "You are a helpful assistant"}, {"role": "user", "content": post.content}, {"role": "user", "content": query} ] 
        
        try: 

            # API 호출 
            response = openai.ChatCompletion.create( 
                 model=model, 
                 messages=messages, 
                 temperature=0.8 ) 
            

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
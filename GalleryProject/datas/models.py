from django.db import models
from django.contrib.auth import get_user_model # 커스텀유저 모델 가져오기

# openApi 사용해서 데이터 불러오기
class DataModel(models.Model):
    title = models.CharField(max_length=200) # TITLE 제목
    description = models.CharField(max_length=1000, null=True) # DESCRIPTION 소개(설명)
    image = models.URLField(max_length=200, null=True) # IAMGE_OBJECT 이미지주소
    pageUrl = models.URLField(max_length=200, null=True) # URL 홈페이지 주소
    author = models.CharField(max_length=200, null=True) # AUTHOR 작가
    period = models.CharField(max_length=200, null=True) # PERIOD 기간
    time = models.CharField(max_length=200, null=True) # EVENT_PERIOD 관람시간
    place = models.CharField(max_length=200, null=True) # CNTC_INSTT_NM 장소
    contact = models.CharField(max_length=200, null=True) # CONTACT_POINT 전화번호
    audience = models.CharField(max_length=200, null=True) # AUDIENCE 전체관람

    def scrap_count(self):
        return self.scrap_set.count()


# 전시 스크랩 기능
User = get_user_model()

class Scrap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scraps')
    data = models.ForeignKey(DataModel, on_delete=models.CASCADE)  # 데이터 모델과 연결
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 동일한 사용자가 동일한 데이터 중복으로 스크랩하지 못하게 함
        unique_together = ['user', 'data'] 

# 댓글 
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',  default="")
    username = models.CharField(max_length=150, blank=True, editable=False)
    profile = models.URLField(max_length=200, blank=True, editable=False) 
    comment = models.CharField(verbose_name="댓글", max_length=128)
    data = models.ForeignKey(DataModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.comment
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.username  # 유저네임을 자동으로 설정
        if not self.profile and hasattr(self.user, 'profile'):
            self.profile = self.user.profile.url 
        super().save(*args, **kwargs)
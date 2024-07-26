from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Post(models.Model) : 
    title = models.CharField(verbose_name="제목", max_length=128, null=False)
    content = models.TextField(verbose_name="내용", null=False) 
    img = models.ImageField(verbose_name="사진", blank=True, upload_to='posts_photo', default='posts_photo/post_default.png')
    view_at = models.DateTimeField(verbose_name="관람일", auto_now_add=True)
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='posts_posts')
    username = models.CharField(max_length=150, blank=True, editable=False)
    profile = models.URLField(max_length=200, blank=True, editable=False) 
    nickname = models.CharField(max_length=150, blank=True, editable=False)
    created_at2 = models.DateTimeField(verbose_name="작성일2", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
     # 제목 15글자 제한
    def save(self, *args, **kwargs):
        if len(self.title) > 15:
            raise ValidationError("제목은 15글자를 초과할 수 없습니다.")
        if not self.username:
            self.username = self.writer.username  # 유저네임을 자동으로 설정
        if not self.nickname and self.writer:
            self.nickname = self.writer.nickname  # 닉네임을 자동으로 설정
        if not self.profile and hasattr(self.writer, 'profile'):
            self.profile = self.writer.profile.url 
        super(Post, self).save(*args, **kwargs)

    def like_count(self):
        return self.like_set.count()
    
    def __str__(self):
        return self.title
    

# 기록하기 좋아요 기능
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Post 모델과 연결
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)

    def toggle_like(self):
        self.is_liked = not self.is_liked
        self.save()

    class Meta:
        # 동일한 사용자가 동일한 기록을 중복으로 좋아요 누르지 못하게 함
        unique_together = ['user', 'post'] 

# 분석하기
class Analysis(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='analysis_results')
    analysis = models.TextField(verbose_name="분석 결과")
    happiness = models.FloatField(verbose_name="행복 퍼센트", null=True, blank=True, default=0.0)
    sadness = models.FloatField(verbose_name="슬픔 퍼센트", null=True, blank=True, default=0.0)
    anger = models.FloatField(verbose_name="분노 퍼센트", null=True, blank=True, default=0.0)
    anxiety = models.FloatField(verbose_name="불안 퍼센트", null=True, blank=True, default=0.0)
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)

from django.db import models
from django.contrib.auth import get_user_model
from datas.models import DataModel

User = get_user_model()

class Music(models.Model) : 
    title = models.CharField(verbose_name="제목", max_length=200, null=False)
    author = models.CharField(verbose_name="아티스트", max_length=50, null=False)
    content = models.TextField(verbose_name="내용", null=False, max_length=300) 
    image = models.ImageField(verbose_name="이미지", blank=True, upload_to='musics_photo', default='musics_photo/music_default.png')
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=150, blank=True, editable=False)
    profile = models.URLField(max_length=200, blank=True, editable=False) 
    created_at2 = models.DateTimeField(verbose_name="작성일2", auto_now_add=True)
    nickname = models.CharField(max_length=150, blank=True, editable=False)
    data = models.ForeignKey(DataModel, on_delete=models.CASCADE)  # 데이터 모델과 연결

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
       if self.writer:
        self.username = self.writer.username  # 유저네임을 자동으로 설정
        self.nickname = self.writer.nickname  # 닉네임을 항상 최신으로 설정
        if hasattr(self.writer, 'profile'):
            self.profile = self.writer.profile.url
        super().save(*args, **kwargs)

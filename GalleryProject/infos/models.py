from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Info(models.Model) : 
    title = models.CharField(verbose_name="제목", max_length=15, null=False)
    author = models.CharField(verbose_name="작가", max_length=15, null=False)
    content = models.TextField(verbose_name="내용", null=False) 
    image = models.ImageField(verbose_name="이미지", blank=True, upload_to='infos_photo')
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=150, blank=True, editable=False)
    profile = models.URLField(max_length=200, blank=True, editable=False) 

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.writer.username  # 유저네임을 자동으로 설정
        if not self.profile and hasattr(self.writer, 'profile'):
            self.profile = self.writer.profile.url 
        super().save(*args, **kwargs)

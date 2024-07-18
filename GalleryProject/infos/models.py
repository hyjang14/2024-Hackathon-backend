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

    def __str__(self):
        return self.title


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model) : 
    title = models.CharField(verbose_name="제목", max_length=128, null=False)
    content = models.TextField(verbose_name="내용", null=False) 
    img = models.ImageField(verbose_name="사진", blank=True, upload_to='posts_photo')
    view_at = models.DateTimeField(verbose_name="관람일", auto_now_add=True)
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    # likes = models.PositiveIntegerField(verbose_name="좋아요", default=0)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.title

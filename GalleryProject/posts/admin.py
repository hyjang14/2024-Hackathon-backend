from django.contrib import admin
from .models import Post, Analysis, Like

admin.site.register(Post)
admin.site.register(Analysis)
admin.site.register(Like)
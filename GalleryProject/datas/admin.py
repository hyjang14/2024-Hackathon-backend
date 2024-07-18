from django.contrib import admin
from .models import DataModel, Comment, Scrap

admin.site.register(DataModel)
admin.site.register(Scrap)
admin.site.register(Comment)


from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    title = models.CharField('제목', max_length=100, null=False)
    content = models.TextField('내용', max_length=100000, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField('작성일', default=timezone.now)
    modified_at = models.DateTimeField('수정일', default=timezone.now)

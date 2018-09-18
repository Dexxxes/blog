from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models



# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-comment_time']
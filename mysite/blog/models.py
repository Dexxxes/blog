from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

class Blog(models.Model):
    title = models.CharField(max_length=30)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    readed_num = models.IntegerField(default=0)
    last_updated_time = models.DateTimeField(auto_now=True)
    blog_type = models.ForeignKey(BlogType,on_delete=models.DO_NOTHING)

    def __str__(self):
        return '<Blog %s>' % self.title

    class Meta:
        ordering = ['-create_time']

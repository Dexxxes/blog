from django.shortcuts import render,redirect
from .models import *
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm

# Create your views here.
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', '/')  # 获取当前页面url
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        return redirect(referer, '/')
    else:
        return render(request,'error.html',{'msg':comment_form.errors,'redirect_to':referer})
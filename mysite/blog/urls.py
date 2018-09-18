from django.urls import path
from . import views

urlpatterns = [
    path('<int:blog_id>',views.blog_detail,name='blog.detail'),                  #博客详情
    path('type/<int:blog_type_id>',views.blogs_with_type,name='blogs_with_type'),#博客类型分类页
    path('',views.blog_list,name='blog_list'),                                   #博客首页
    path('date/<int:year>/<int:month>',views.blogs_with_dates,name='blogs_with_dates'),#博客时间分类页
]

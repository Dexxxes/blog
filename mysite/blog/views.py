from django.shortcuts import get_object_or_404,render
from .models import *
from django.core.paginator import Paginator
from django.db.models import Count
from django.core.cache import cache
from comment.models import *
from comment.forms import CommentForm

# Create your views here.

#公共函数,将各个视图公共的部分提取出来
def common_func(request,blog_all_list):
    page_num = request.GET.get('page', 1)  # 获取页码
    paginator = Paginator(blog_all_list, 2)  # 每2篇为一页
    page_of_blogs = paginator.get_page(page_num)  # 本页博客
    max_page = paginator.num_pages  # 总页码
    if max_page >= 5:
        if max_page - 2 >= int(page_num) >= 3:
            page_range = range(int(page_num) - 2, int(page_num) + 3)
        elif 1 <= int(page_num) < 3:  # 页码太小时
            page_range = range(1, 6)
        else:
            page_range = range(max_page - 4, max_page + 1)  # 页码太大时
    else:
        page_range = range(1, max_page + 1)

    #统计按月倒序分类时,Blog的数量.
    date_count_dict = {}
    for blog_obj in Blog.objects.dates('create_time','month','DESC'):
        blog_date = Blog.objects.filter(create_time__year=blog_obj.year,create_time__month=blog_obj.month)
        date_count_dict[blog_obj] = blog_date.count()

    context = {}
    context['blogs_count'] = blog_all_list.count()
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = date_count_dict
    return context

#博客首页
def blog_list(request):
    if not cache.get('blog_all_list'):
        blog_all_list = Blog.objects.all()
        cache.set('blog_all_list',blog_all_list,3600)
    blog_all_list = Blog.objects.all()
    context = common_func(request,blog_all_list)
    return render(request,'blog/blog_list.html',context)

#博客详情页
def blog_detail(request,blog_id):
    blog = get_object_or_404(Blog,id=blog_id)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog_id)
    if not request.COOKIES.get('blog_%s_readed' % blog_id):
        blog.readed_num += 1
        blog.save()
    context = {}
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog'] = blog
    context['comments'] = comments
    context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model,'object_id':blog_id})
    response = render(request,'blog/blog_detail.html',context)
    response.set_cookie('blog_%s_readed' % blog_id,'true')
    return  response

#博客类型分类页面
def blogs_with_type(request,blog_type_id):
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = common_func(request,blog_all_list)
    context['blogs_type'] = blog_type
    return render(request,'blog/blogs_with_type.html', context)

#博客时间分类页面
def blogs_with_dates(request,year,month):
    blog_all_list = Blog.objects.filter(create_time__year=year,create_time__month=month)
    context = common_func(request,blog_all_list)
    return render(request,'blog/blogs_with_type.html', context)

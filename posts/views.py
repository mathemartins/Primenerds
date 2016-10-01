try:
    from urllib import quote_plus
except:
    pass

from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.safestring import mark_safe

from accounts.forms import UserLoginForm, UserRegisterForm
from accounts.models import MyUser, MyUserManager

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django_filters import FilterSet, CharFilter, NumberFilter
from comments.forms import CommentForm

# Create your views here.
from comments.models import Comment
from posts.forms import PostForm
from posts.models import Post
#from posts.utils import get_read_time
from analytics.models import PageView
from analytics.signals import page_view
from questions.models import Question
from videos.models import Video, Category

def post_create(request):
    if not request.user.is_staff: #or not request.user.is_admin:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        #message success pops out
        messages.success(request, 'Post Created Successfully!')
        return HttpResponseRedirect(instance.get_absolute_url())

    if request.method == "POST":
        print request.POST
    context = {
        "form": form,
    }
    return render (request, "post_form.html", context)



def post_detail(request, slug=None): #retrieve data
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff: #or not request.user.is_admin:
            raise Http404
    share_string = quote_plus(instance.content)

    #print (get_read_time(instance.content))
    #print (get_read_time(instance.get_markdown()))
    initial_data = {
        "content_type":instance.get_content_type,
        "object_id": instance.id,
    }
    #queryset_list = Post.objects.active() #.order_by("-timestamp")
    #paginator = Paginator(queryset_list, 10) # Show 10 comments per page
    form = CommentForm(request.POST or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated():
        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        parent_obj = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                user = request.user,
                content_type = content_type,
                object_id = obj_id,
                content = content_data,
                parent = parent_obj,
            )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments
    context = {
        "title":instance.title,
        "instance":instance,
        "share_string":share_string,
        "comments":comments,
        "comment_form":form,
    }
    return render (request, "post_detail.html", context)
    #return HttpResponse("<h2> Detail</h2>")


def post_list(request): #list items #this one is for homepage
    today = timezone.now().date()
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    print (request.user.is_authenticated())
    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)

    if request.user.is_staff: #or request.user.is_admin:
        queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 1) # Show 1 blog(s) per page
    page_request_var = 'page'
    page = request.GET.get( page_request_var )
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if next:
                return HttpResponseRedirect(next)
            print (request.user.is_authenticated())

            #redirect url link comes in here
            return redirect("/")
            action_url = reverse("login")
            extra_form_link = "Upgrade your account today <a href='%s'>here</a>!" %(reverse("account_upgrade"))

    context = {
            "object_list":queryset,
            "title":"List",
            "form":form,
    		"title":title,
            "page_request_var":page_request_var,
            "today":today,
    }

    return render (request, "post_list.html", context)
    #return HttpResponse("<h2> List </h2>")




def post_update(request, slug=None): #update data
    if not request.user.is_staff: #or not request.user.is_admin:
        #defaults.page_not_found(request, template_name='404.html')
        raise Http404

    instance = get_object_or_404(Post, slug=slug)

    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print form.cleaned_data.get("title")
        instance.save()
        messages.success(request, "<a href='#'>Post</a> Saved Successfully!", extra_tags = 'html_safe')
        #message success pops out
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title":instance.title,
        "instance":instance,
        "form":form,
    }
    return render (request, "post_form.html", context)

def post_delete(request, slug=None): #delete data
    if not request.user.is_staff: #or not request.user.is_admin:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "<a href='#'>Post</a> Deleted Successfully!")
    #message success pops out
    return redirect("posts:list")


#####################################################################################
#         This is for blog_list.html alone                                          #
#                                                                                   #
#####################################################################################

class PostFilter(FilterSet):
    """docstring for PostFilter"""
    title = CharFilter(name='title__title', lookup_type='icontains')
    class Meta:
        model = Post
        fields =[
            'title',
            #'content',
            'user__first_name',
            'user__last_name',
        ]

    #def __init__(self, arg):
    #    super(PostFilter, self).__init__()
    #    self.arg = arg


def blog_list(request): #list items #this one is for homepage
    today = timezone.now().date()
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    if request.user.is_staff: #or request.user.is_admin:
        queryset_list = Post.objects.all()
        f = PostFilter(request.GET, queryset=queryset_list)
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
            ).distinct()
    paginator = Paginator(queryset_list, 20) # Show 20 blogs per page
    page_request_var = 'page'
    page = request.GET.get( page_request_var )
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
            "object_list":queryset,
            #"obj_list":f,
            "title":"List",
            "page_request_var":page_request_var,
            "today":today,
    }

    return render (request, "blog_list.html", context)
    #return HttpResponse("<h2> List </h2>")


def about_us(request):
    context = {}
    return render(request, "about_us.html", context)

def services(request):
    context = {}
    return render(request, "service.html", context)

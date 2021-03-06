from urllib import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.
from posts.forms import PostForm
from posts.models import Post

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
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
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    context = {
        "title":instance.title,
        "instance":instance,
        "share_string":share_string,
    }
    return render (request, "post_detail.html", context)
    #return HttpResponse("<h2> Detail</h2>")


def post_list(request): #list items #this one is for homepage
    today = timezone.now().date()
    queryset_list = Post.objects.active() #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 8) # Show 2 blogs per page
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
            "title":"List",
            "page_request_var":page_request_var,
            "today":today,
    }
    
    #if request.user.is_authenticated():
    #   context = {
    #        "title":"My User List"
    #    }
    #else:
    #    context = {
    #        "title":"List"
    #    }
    return render (request, "blog_list.html", context)
    #return HttpResponse("<h2> List </h2>")

def post_update(request, slug=None): #update data
    if not request.user.is_staff or not request.user.is_superuser:
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
    if not request.user.is_staff or not request.user.is_superuser:
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

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
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
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.content)

    context = {
        "title":instance.title,
        "instance":instance,
        "share_string":share_string,
    }
    return render (request, "post_detail.html", context)
    #return HttpResponse("<h2> Detail</h2>")


def post_update(request, slug=None): #update data
    if not request.user.is_staff or not request.user.is_superuser:
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
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "<a href='#'>Post</a> Deleted Successfully!")
    #message success pops out
    return redirect("posts:list")

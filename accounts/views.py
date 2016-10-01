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
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.safestring import mark_safe

from accounts.forms import UserLoginForm, UserRegisterForm
from accounts.models import MyUser, MyUserManager

from analytics.models import PageView
from analytics.signals import page_view
from questions.models import Question
from videos.models import Video, Category

# Create your views here.

def logged_in_homepage(request):
	try:
	    page_view.send(
	    	request.user,
	    	page_path=request.get_full_path()
	    	)
	    if request.user.is_authenticated():
	    	page_view_objs = request.user.pageview_set.get_videos()[:6]

	    	recent_videos = []
	    	for obj in page_view_objs:
	    		if not obj.primary_object in recent_videos:
	    			#print obj.primary_object
	    			recent_videos.append(obj.primary_object)
	    	recent_questions = Question.objects.recent()

	    	#top items
	    	video_type = ContentType.objects.get_for_model(Video)
	    	popular_videos_list = PageView.objects.filter(primary_content_type=video_type)\
	    	 .values("primary_object_id")\
	    	 .annotate(the_count=Count("primary_object_id"))\
	    	 .order_by("-the_count")[:4]
	    	popular_videos = []
	    	for item in popular_videos_list:
	    		try:
	    			new_video = Video.objects.get(id=item['primary_object_id'])
	    			popular_videos.append(new_video)
	    		except:
	    			pass

	    	random_videos = Video.objects.all().order_by('?')[:6]
	    	#print popular_videos
	    	# one item
	    	#PageView.objects.filter(primary_content_type=video_type, primary_object_id=21).count()


	    	context = {
	    		"random_videos": random_videos,
	    		"recent_videos": recent_videos,
	    		"recent_questions": recent_questions,
	    		"popular_videos": popular_videos,
	    		}
	    	template = "logged_in/home.html"
	    	#return HttpResponseRedirect('/dashboard/')
	    else:
	    	featured_categories = Category.objects.get_featured()
	    	featured_videos = Video.objects.get_featured()
	    	login_form = LoginForm()
	    	register_form = RegisterForm()
	    	template = "post_list.html"
	    	context = {
	    		"register_form": register_form,
	    		"login_form": login_form,
	    		"featured_videos":featured_videos,
	    		"featured_categories": featured_categories,
	    	}

	    return render(request,template,context)
	except:
		raise Http404

def auth_login(request):
	print (request.user.is_authenticated())
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
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
			return redirect("logged_in")
			action_url = reverse("login")
			extra_form_link = "Upgrade your account today <a href='%s'>here</a>!" %(reverse("account_upgrade"))

	context = {
		"form":form,
		"title":title,
	}
	return render(request, "form.html", context)


def register_view(request):
	print (request.user.is_authenticated())
	if request.user.is_authenticated():
		raise Http404
	next = request.GET.get('next')
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		#MyUser = form.save(commit=False)
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email')
		password2 = form.cleaned_data.get('password2')

		#MyUser.objects.create_user(username=username, email=email, password=password)
		new_user = MyUser()
		new_user.username = username
		new_user.email = email
		new_user.set_password(password2) #RIGHT
		new_user.save()

		new_user = authenticate(username=username, password=password2)
		login(request, new_user)
		#return redirect("login")
		if next:
			return redirect(next)
		# Add message for success
		#return something good
		return redirect('/home')
		#return HttpResponseRedirect(reverse('/'))

	#action_url = reverse("register")

	context = {
		'form':form,
		'title':title,
	}
	return render(request, "form.html", context)


def auth_logout(request):
	logout(request)
	context = {}
	return redirect("/")

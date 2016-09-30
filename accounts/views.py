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

# Create your views here.

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
			return redirect("/")
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
		return redirect('/')
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

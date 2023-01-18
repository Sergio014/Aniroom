from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.contrib.auth.models import User

from .auth_tools import AuthTools
from .models import Profile, Post
from .forms import ProfileImageForm, PostForm

# Create your views here.
def register_view(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.POST:
		form_data = request.POST
		user_data = {
			'username': ''.join(form_data['username']),
			'first_name': form_data["fname"],
			'last_name': form_data["lname"],
			'password': form_data["password"],
			'email': form_data["email"]
		}
		user = AuthTools.register(user_data)
		if user["is_new"] == False:
			if user["invalid"] == "username":
				in_eror = {'text_u': 'Username is already used'}
				return render(request, 'User/sign_up.html', context=in_eror)
			new_eror = {'text': 'This email is already used'}
			return render(request, 'User/sign_up.html', context=new_eror)
		return redirect('/login/')
	return render(request, "User/sign_up.html")

def login_view(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.POST:
		data = request.POST
		username = data.get('username', False)
		password = data.get('password', False)
		user = AuthTools.authenticate(username, password)
		if user is None:
			in_eror = {'text_u': 'Incorect username or password!'}
			return render(request, 'User/log_in_page.html', context=in_eror)
		AuthTools.login(request, user)		
		profile_data = {
			'user': None,
			"bio": None,
			"website_url": None,
		}
		AuthTools.profile_register(user, profile_data)
		return redirect('/')
	return render(request, 'User/log_in_page.html')
	
def profile_view(request):
	user = request.user
	if user.is_authenticated:
		profile = Profile.objects.get(user=user)
		try:
			posts = Post.objects.filter(owner=profile)
			print(posts)
			user_data = {
				"user": user,
				"profile": profile,
				'posts': posts,
			}
		except:
			user_data = {
				"user": user,
				"profile": profile,
			}
		return render(request, 'User/profile.html', context=user_data)
	return render(request, 'User/log_in_page.html')
	
def edit_profile_view(request):
	user = request.user
	if not user.is_authenticated:
		return redirect('/login/')
	profile = Profile.objects.get(user=user)
	form = ProfileImageForm()
	user_data = {
		"user": user,
		'profile': profile,
		'form': form,
	}
	if request.POST:
		form_data = request.POST
		form = ProfileImageForm(request.POST, request.FILES)
		if form.is_valid():
			if form.cleaned_data["profile_image"] is not None:
				img = form.cleaned_data.get("profile_image")
				profile.profile_image = img
				profile.save()
				return render(request, "User/profile.html", context=user_data)
			else:
				user.username = "".join(form_data['username'])
				user.first_name = form_data["first_name"]
				user.last_name = form_data["last_name"]
				profile.bio = form_data["bio"]
				profile.website_url = form_data["website_url"]
				profile.save()
				user.save()
				return render(request, 'User/profile.html', context=user_data)
	return render(request, "User/edit_profile.html", context=user_data)
	
def add_post_view(request):
	if not user.is_authenticated:
		return redirect('/login/')
	form = PostForm()
	user = request.user
	profile = Profile.objects.get(user=user)
	profile_data = {
		'user': user,
		'profile': profile,
		'form': form,
	}
	if request.POST:
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			print(form.cleaned_data)
			image = form.cleaned_data.get("image")
			info = form.cleaned_data.get("info")
			Post.objects.create(image=image, info=info, owner=profile_data["profile"]).save()
			return redirect('/')
	return render(request, "User/add_post.html", profile_data)
	
def logout_view(request):
	if not request.user.is_authenticated:
		return redirect('/login/')
	if request.POST:
		AuthTools.logout(request)
		return redirect('/login/')
	return render(request, "User/logout.html")

def whatch_profile_view(request, username):
	if not request.user.is_authenticated:
		return redirect('/login/')
	elif request.user.username == username:
		return redirect('/')
	user = User.objects.get(username=username)
	context = {
		'user': user,
		'profile': Profile.objects.get(user=user),
	}
	return render(request, "User/watch_profile.html", context)
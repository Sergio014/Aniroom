from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.http import Http404

from .auth_tools import AuthTools
from .models import Profile, Post, UserFollowing, Comment, Like, Feedback, Blocked
from .forms import ProfileImageForm, PostForm

# Create your views here.
def register_view(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.POST:
		form_data = request.POST
		if not form_data['password'] == form_data['password2']:
			return render(request, "User/register.html",  context={'inc_pass': "Passwords do not match."})
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
				in_eror = {'username_excist': 'Username is already used'}
				return render(request, 'User/register.html', context=in_eror)
			new_eror = {'email_alr_excist': 'This email is already used'}
			return render(request, 'User/register.html', context=new_eror)
		return redirect('/login/')
	return render(request, "User/register.html")

def login_view(request):
	if request.user.is_authenticated:
		return redirect('/')
	if request.POST:
		data = request.POST
		username = data.get('username', False)
		password = data.get('password', False)
		user = AuthTools.authenticate(username, password)
		if user is None:
			in_eror = {'inc_username_or_pass': 'Incorect username or password!'}
			return render(request, 'User/login.html', context=in_eror)
		AuthTools.login(request, user)		
		profile_data = {
			'user': None,
			"bio": None,
			"website_url": None,
		}
		AuthTools.profile_register(user, profile_data)
		return redirect('/')
	return render(request, 'User/login.html')
	
def profile_view(request):
	user = request.user
	if user.is_authenticated:
		profile = Profile.objects.get(user=user)
		try:
			posts = Post.objects.filter(owner=profile)
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
	return redirect("/login/")
	
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
			      if profile.profile_image:
			      	profile.profile_image.delete()
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
	if not request.user.is_authenticated:
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
			post = form.save(commit=False)
			post.owner = profile_data["profile"]
			post.save()
			form.save_m2m()
			return redirect('/')
	return render(request, "User/add_post.html", profile_data)

def whatch_profile_view(request, username):
	if not request.user.is_authenticated:
		return redirect('/login/')
	elif request.user.username == username:
		return redirect('/')
	watcher = Profile.objects.get(user=request.user)
	user = User.objects.get(username=username)
	profile = Profile.objects.get(user=user)
	context = {
		'user': user,
		'profile': profile,
		'followed': AuthTools.is_followed(watcher, profile),
	}
	if AuthTools.was_blocked(watcher, profile) or AuthTools.is_blocked(watcher, profile):
		raise Http404
	if request.POST:
		try:
			UserFollowing.objects.get(
				user=watcher,
				following_user=profile
			).delete()
			context["followed"] = False
		except:
			UserFollowing.objects.create(
				user=watcher,
				following_user=context['profile']
			)
			context["followed"] = True
		return render(request, "User/watch_profile.html", context)
	return render(request, "User/watch_profile.html", context)
	
def post_view(request, username, pk):
	if not request.user.is_authenticated:
		return redirect('/login/')
	user = User.objects.get(username=username)
	profile = Profile.objects.get(user=user)
	post = profile.post.get(pk=pk)
	watcher = Profile.objects.get(user=request.user)
	try:
		comments = Comment.objects.filter(post=post)
	except:
		comments = []
	context = {
		"profile": profile,
		'post': post,
		"watcher": watcher,
		"is_owner": AuthTools.is_owner(user, request),
		"comments": comments,
		"liked": AuthTools.is_liked(watcher, post),
	}
	if request.POST and "comment" in request.POST:
		text = request.POST['comment']
		Comment.objects.create(text=text, owner=watcher, post=post)
		context["comments"] = Comment.objects.filter(post=post)
		return render(request, "User/post.html", context)
	elif request.POST and "delete" in request.POST and context["is_owner"]:
		post.image.delete()
		post.delete()
		return redirect("/")
	elif "unlike" in request.POST:
		Like.objects.get(owner=watcher, post=post).delete()
		context["liked"] = False
		return render(request, "User/post.html", context)
	elif "like" in request.POST:
		Like.objects.create(owner=watcher, post=post)
		context["liked"] = True
		return render(request, "User/post.html", context)
	elif "delete_comment" in request.POST:
		pk = request.POST["pk"]
		Comment.objects.get(pk=pk).delete()
		try:
			Comment.objects.filter(post=post)
			context["comments"]  = comments
		except:
			context["comments"]  = []
		return render(request, "User/post.html", context)
	return render(request, "User/post.html", context)
	
def settings_view(request):
	user = request.user
	if not user.is_authenticated:
		return redirect("/login/")
	profile = Profile.objects.get(user=user)
	if "logout" in request.POST:
		AuthTools.logout(request)
		return redirect('/login/')
	elif "my_likes" in request.POST:
		
		posts = Post.objects.filter(likes__owner=profile)
		context = {
			"posts": posts,
		}
		return render(request, "User/liked_posts.html", context)
	elif "blocked_users" in request.POST:
		context = {
			'blocked_users': profile.user_who_block.all()
		}
		return render(request, "User/blocked_users.html", context)
	elif "send_feedback" in request.POST:
		return render(request, "User/send_feedback.html")
	elif "text" in request.POST:
		text = request.POST["text"]
		Feedback.objects.create(text=text)
		return render(request, "User/settings.html")
	elif "unblock" in request.POST:
		username = request.POST["unblock"].split()[1]
		blocked_user = Profile.objects.get(user__username=username)
		Blocked.objects.filter(user=profile, blocked_user=blocked_user).delete()
		return render(request, "User/settings.html")
	return render(request, "User/settings.html")
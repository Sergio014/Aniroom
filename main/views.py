from django.shortcuts import render

import random

from User.models import Post, Profile

def home_view(request):
	watcher = Profile.objects.get(user=request.user)
	try:
		posts = Post.objects.filter(tags__name__in=[f"{watcher.fav_anime}"]).order_by('?')
	except:
		posts = Post.objects.all()
	context = {
		"posts": posts,
	}
	return render(request, "main/home.html", context)
	
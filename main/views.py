from django.shortcuts import render

import random

from User.models import Post, Profile
# Create your views here.

def home_view(request):
	posts = list(Post.objects.all())
	random_posts = random.sample(posts, 3)
	context = {
		"posts": random_posts,
		"profile": Profile.objects.last(),
	}
	return render(request, "main/home.html", context)
	
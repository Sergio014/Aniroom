from django.shortcuts import render
from django.db.models import Q

from User.models import Post

def search_view(request):
	search_post = request.GET.get("search")
	if search_post:
	   posts = Post.objects.filter(Q(info__icontains=search_post) | Q(tags__name__in=[f"{search_post}"]))
	else:
		posts = Post.objects.all()
	return render(request, "searching/search.html", {"posts": posts})
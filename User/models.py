from django.db import models
from django.contrib.auth.models import User 

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, default=None)
	bio = models.TextField(blank=True, null=True)
	website_url = models.CharField(max_length=40, blank=True, null=True)
	
	@property
	def posts_count(self):
		return self.post.all().count()
		
	@property
	def followers_count(self):
		return self.followers.all().count()
		
	@property
	def following_count(self):
		return self.following.all().count()

	def __str__(self):
		return f"{self.user.username}"

class UserFollowing(models.Model):
    user = models.ForeignKey(Profile, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(Profile, related_name="followers", on_delete=models.CASCADE)

class Post(models.Model):
	image = models.ImageField(upload_to='post_images/')
	info = models.CharField(max_length=255, null=True, blank=True)
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="post")
	
	@property
	def likes_count(self):
		return self.likes.all().count()
		
	def __str__(self):
		return f"{self.info}"
		
class Like(models.Model):
	owner = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
	
	def __str__(self):
		return f"{self.owner} liked {self.post}."

class Comment(models.Model):
	text = models.CharField(max_length=255)
	owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
	
	def __str__(self):
		return f"{self.owner} commented {self.post}."
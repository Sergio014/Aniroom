from django.db import models  
from django.forms import fields  
from .models import Profile, Post
from django import forms
  
  
class ProfileImageForm(forms.ModelForm):  
    class Meta:
        model = Profile
        profile_image = forms.ImageField(widget=forms.FileInput(attrs={'name':'profile_image'}))
        fields = ["profile_image"]

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = "__all__"
		exclude = ["owner"]
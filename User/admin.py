from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(Profile)

admin.site.register(Post)

admin.site.register(Like)

admin.site.register(Comment)

admin.site.register(UserFollowing)

admin.site.register(Blocked)

admin.site.register(Feedback)
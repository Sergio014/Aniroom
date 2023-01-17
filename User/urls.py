from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import register_view, profile_view, login_view, edit_profile_view, add_post_view


app_name = 'User'

urlpatterns = [
	path("register/", register_view, name="register"),
	path("login/", login_view, name="login"),
	path("profile/", profile_view, name="profile"),
	path("profile/edit/", edit_profile_view, name="edit_profile"),
	path("add_post/", add_post_view, name="add_post"),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
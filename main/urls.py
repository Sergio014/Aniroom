from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import home_view

app_name = 'main'

urlpatterns = [
	path("", home_view, name="home"),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
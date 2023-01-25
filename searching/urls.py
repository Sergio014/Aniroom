from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import search_view

app_name = 'searching'

urlpatterns = [
	path("", search_view, name="search"),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
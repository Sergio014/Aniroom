from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.PostsListView.as_view())
]
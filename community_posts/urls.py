from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.posts_list_create),
    path('posts/<uuid:post_id>/', views.post_detail),  # GET/DELETE
    path('posts/<uuid:post_id>/comments/', views.post_comments),
]
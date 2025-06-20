from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.oauth_login),
    path("logout/", views.oauth_logout),
    path("callback/", views.oauth_callback),
    path("get-role/", views.get_current_user_role),
]

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.InvitationAdapter.createInvitation),
    path('activate', views.InvitationAdapter.use_invitation),
]
from django.urls import path
from . import views

urlpatterns = [
    path('send-test-email/', views.test_email),
]
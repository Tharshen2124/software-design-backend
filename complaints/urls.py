from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create),
    path("custom-admin/", views.get_all_complaints),
    path("custom-admin/<int:complaint_id>", views.get_complaint),
    path("government/", views.get_all_filtered_complaints),
    path("government/<int:complaint_id>", views.get_fitlered_complaint),
    path("update-status/<int:complaint_id>/", views.update_complaint_status),
]
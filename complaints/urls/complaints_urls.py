from django.urls import path
from complaints.views import complaint_views

urlpatterns = [
    path("create/", complaint_views.create),
    path("custom-admin/", complaint_views.get_all_complaints),
    path("custom-admin/<int:complaint_id>/", complaint_views.get_complaint),
    path("government/", complaint_views.get_all_filtered_complaints),
    path("government/<int:complaint_id>/", complaint_views.get_fitlered_complaint),
    path("update-status/<int:complaint_id>/", complaint_views.update_complaint_status),
]

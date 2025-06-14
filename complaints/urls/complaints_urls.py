from django.urls import path
from complaints.views import complaint_views

urlpatterns = [
    path("citizen/<int:citizen_id>/", complaint_views.get_all_complaints_for_citizen),
    path("citizen/complaint/<int:complaint_id>/", complaint_views.get_complaint_for_citizen),
    path("approved/", complaint_views.get_all_approved_complaints),
    path("create/", complaint_views.create),
    path("custom-admin/", complaint_views.get_all_complaints),
    path("custom-admin/<int:complaint_id>/", complaint_views.get_complaint),
    path("government/", complaint_views.get_all_filtered_complaints),
    path("government/<int:complaint_id>/", complaint_views.get_fitlered_complaint),
    path("update-status/<int:complaint_id>/", complaint_views.update_complaint_status),
]

from django.urls import path
from complaints.views import maintenance_views

urlpatterns = [
    path("create/", maintenance_views.create),
    # path("custom-admin/", maintenance_views.get_all_maintenance_plans),
    # path("custom-admin/<int:maintenance_id>/", maintenance_views.get_maintenance_plan),
    # path("government/", maintenance_views.get_all_filtered_maintenance_plans),
    # path("government/<int:maintenance_id>/", maintenance_views.get_filtered_maintenance_plan),
    # path("update-status/<int:maintenance_id>/", maintenance_views.update_maintenance_plan_status),
]

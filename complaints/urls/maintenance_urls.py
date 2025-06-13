from django.urls import path
from complaints.views import maintenance_views

urlpatterns = [
    path("create/", maintenance_views.create),
    path("company/<str:maintenance_company_id>/", maintenance_views.get_all_maintenance_projects_for_company),
    path("project/<str:project_id>/", maintenance_views.get_maintenance_projects_for_company),
    path("update/", maintenance_views.update),
]

from django.http import JsonResponse
from clients.supabase_client import supabase
from django.views.decorators.csrf import csrf_exempt
from ..builders.maintenance_builder import MaintenanceProjectBuilder
from ..case_director import CaseDirector
from ..adapters.maintenance_adapter import MaintenanceProjectAdapter

@csrf_exempt
def create(request):
    try:
        data = MaintenanceProjectAdapter.get_data(request)
    except ValueError as valueError:
        return JsonResponse({
            "error": "Invalid form data",
            "details": str(valueError)
        }, status=400)
    
    try:
        builder = MaintenanceProjectBuilder()
        director = CaseDirector()
        maintenance_data = director.buildMaintenancePlan(builder, data)

        supabase.table("maintenance_projects").insert(maintenance_data).execute()

        return JsonResponse({
            "message": "Successfully uploaded maintenance project",
        }, status=201)
    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=500)

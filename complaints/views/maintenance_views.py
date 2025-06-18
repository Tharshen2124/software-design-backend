from django.http import JsonResponse
from clients.supabase_client import supabase
from django.views.decorators.csrf import csrf_exempt
from ..builders.maintenance_builder import MaintenanceProjectBuilder
from ..case_director import CaseDirector
from ..adapters.maintenance_adapter import MaintenanceProjectAdapter
from clients.cloudinary_client import CloudinaryClient
from ..status_enum import Status

@csrf_exempt
def create(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

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
        maintenance_data = director.buildMaintenanceProject(builder, data)
        # Validate the maintenance data
        if not maintenance_data:
            return JsonResponse({"error": "Invalid maintenance project data."}, status=400)
        
        # Insert the maintenance project into the database
        result = supabase.table("maintenance_projects").insert({
            "project_title": maintenance_data["project_title"],
            "project_description": maintenance_data["project_description"],
            "status": maintenance_data["status"],
            "maintenance_company_id": maintenance_data["maintenance_company_id"]
        }).execute()
        
        new_maintenance_project_id = result.data[0]["maintenance_project_id"]
        
        update_result = supabase.table("complaints") \
            .update({
                "maintenance_project_id": new_maintenance_project_id,
                "status": Status.IN_PROGRESS.value
            }) \
            .in_("complaint_id", maintenance_data["complaint_ids"]) \
            .is_("maintenance_project_id", None) \
            .execute()

        return JsonResponse({
            "message": "Maintenance project created and complaints updated.",
            "maintenance_project_id": new_maintenance_project_id
        }, status=201)
    
    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=500)

@csrf_exempt
def get_all_maintenance_projects_for_company(request, maintenance_company_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET is only allowed."}, status=405)

    # retrieve maintenance projets that have status "pending" and another retrival logic for the status "in_progress"
    try:
        pending_projects = supabase.table('maintenance_projects') \
            .select('*, complaints(*)') \
            .eq('maintenance_company_id', str(maintenance_company_id)) \
            .eq('status', Status.PENDING.value) \
            .execute()
        
        # Retrieve in-progress projects
        in_progress_projects = supabase.table('maintenance_projects') \
            .select('*, complaints(*)') \
            .eq('maintenance_company_id', str(maintenance_company_id)) \
            .eq('status', Status.IN_PROGRESS.value) \
            .execute()
        if not in_progress_projects.data and not pending_projects.data:
            return JsonResponse({"message": "No maintenance projects found for this company."}, status=404)

        return JsonResponse({
            "pending_projects": pending_projects.data,
            "in_progress_projects": in_progress_projects.data
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=500)

@csrf_exempt
def get_maintenance_projects_for_company(request, project_id):
    if request.method != "GET":
        return JsonResponse({"error": "GET is only allowed."}, status=405)

    try:
        response = supabase.table('maintenance_projects') \
            .select('*, complaints(*)') \
            .eq('maintenance_project_id', str(project_id)) \
            .single() \
            .execute()
            
        return JsonResponse({
            "maintenance_project": response.data
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=500)
    
@csrf_exempt
def update(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)

    try:
        data = MaintenanceProjectAdapter.get_data_for_update(request)
        
        status = data.status.value
        image_url = data.image_url
        maintenance_project_id = data.maintenance_project_id
        follow_up = data.follow_up

        print(f"Updating maintenance project {maintenance_project_id} with status: \n {status},\n image_url: {image_url},\n follow_up: {follow_up}")

        if status == Status.IN_PROGRESS.value:
            print("Updating status to IN_PROGRESS")
            supabase.table("maintenance_projects") \
                .update({"status": status}) \
                .eq("maintenance_project_id", maintenance_project_id) \
                .execute()
        elif status == Status.RESOLVED.value:
            print("Updating status to RESOLVED")
            supabase.table("maintenance_projects") \
                .update({
                    "status": status, 
                    "project_image_url": image_url,
                    "follow_up": follow_up
                }) \
                .eq("maintenance_project_id", maintenance_project_id) \
                .execute()
            
            supabase.table("complaints") \
                .update({"status": Status.RESOLVED.value}) \
                .eq("maintenance_project_id", maintenance_project_id) \
                .execute()

        return JsonResponse({
            "message": "Maintenance project status updated successfully."
        }, status=200)

    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=500)

# retrieve all maintenance projects where each has their list of complaints and the maintenance company associated to a maintenance project
@csrf_exempt
def get_all_maintenance_projects(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET is only allowed."}, status=405)

    try:
        response = supabase.table('maintenance_projects') \
            .select('*, complaints(*), maintenance_companies(*, users(*))') \
            .execute()
        
        if not response.data:
            return JsonResponse({"message": "No maintenance projects found."}, status=404)

        return JsonResponse({
            "maintenance_projects": response.data
        }, safe=False, status=200)

    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=500)
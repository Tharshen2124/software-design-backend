from django.http import JsonResponse
from clients.supabase_client import supabase
from django.views.decorators.csrf import csrf_exempt
from ..builders.complaint_builder import ComplaintBuilder
from ..case_director import CaseDirector
from ..adapters.complaint_adapter import ComplaintAdapter

@csrf_exempt
def create(request):
    try:
        data = ComplaintAdapter.get_data(request)
    except ValueError as valueError:
        return JsonResponse({
            "error": "Invalid form data",
            "details": str(valueError)
        }, status=400)
    
    try:
        builder = ComplaintBuilder()
        director = CaseDirector()
        complaint_data = director.buildComplaints(builder, data)

        supabase.table("complaints").insert(complaint_data).execute()

        return JsonResponse({
            "message": "Successfully uploaded complaint",
        }, status=201)
    except Exception as e:
        return JsonResponse({
            "error": "An unexpected error occurred",
            "details": str(e)
        }, status=500)

@csrf_exempt
def get_all_complaints(request):
    response = supabase.table('complaints') \
        .select('*, citizens(*, users(*))') \
        .eq('status', 'pending')\
        .execute()
    return JsonResponse({
        "complaints": response.data
    }, safe=False)

@csrf_exempt
def get_complaint(request, complaint_id):
    response = supabase.table('complaints')\
        .select('*, citizens(*, users(*))')\
        .eq('complaint_id', str(complaint_id))\
        .single()\
        .execute()

    return JsonResponse({
        "complaint": response.data
    }, safe=False)

@csrf_exempt
def get_all_filtered_complaints(request):
    response = supabase.table('complaints')\
        .select('*, citizens(*, users(*))')\
        .eq('status', 'filtered')\
        .execute()

    return JsonResponse({
        "filtered_complaints": response.data
    }, safe=False)

@csrf_exempt
def get_fitlered_complaint(request, complaint_id):
    response = supabase.table('complaints')\
        .select('*, citizens(*, users(*))')\
        .eq('id', str(complaint_id))\
        .eq('status', 'filtered')\
        .single()\
        .execute()

    return JsonResponse({
        "filtered_complaint": response.data
    }, safe=False)

@csrf_exempt
def update_complaint_status(request, complaint_id):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

    new_status = request.POST.get("status")

    if not complaint_id or not new_status:
        return JsonResponse({"error": "Missing complaint_id or status."}, status=400)

    try:
        response = supabase.table("complaints") \
            .update({"status": new_status}) \
            .eq("complaint_id", complaint_id) \
            .execute()

        return JsonResponse({
            "message": "Complaint status updated successfully.",
            "data": response.data
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



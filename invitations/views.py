import json
from django.http import HttpResponse, JsonResponse
from .invitationManager import InvitationManager
from django.views.decorators.csrf import csrf_exempt
from clients.supabase_client import supabase

manager = InvitationManager() # make it global

class InvitationAdapter:
    @staticmethod
    @csrf_exempt
    def createInvitation(request):
        try: 
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        # if valid data
        email = data.get("email")
        role = data.get("role")

        # error handling if there's no valid response
        if not email or not role:
            return JsonResponse({"error": "Missing data"}, status=400)
        
        
        manager.create_invitation(email,role)

        response = supabase.table('invitations').select('invitation_id').eq('email', email).execute()
        link = response.data[0]['invitation_id']

        isSuccess = manager.send_invitation(email, link)

        if isSuccess:
            return JsonResponse({"message": "Invitation sent successfully"}, status=200)
        
        else:
            return JsonResponse({"error": "Failed to send invitation"}, status=500)
import json
from django.http import HttpResponse, JsonResponse
from .invitationManager import InvitationManager
from django.views.decorators.csrf import csrf_exempt

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
        link = data.get("link")

        # error handling if there's no valid response
        if not email or not link:
            return JsonResponse({"error": "Missing data"}, status=400)
        
        # will return boolean
        manager = InvitationManager()
        isSuccess = manager.send_invitation(email, link)

        if isSuccess:
            return JsonResponse({"message": "Invitation sent successfully"}, status=200)
        
        else:
            return JsonResponse({"error": "Failed to send invitation"}, status=500)
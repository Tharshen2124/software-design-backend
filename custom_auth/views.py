from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import JsonResponse
from clients.supabase_client import supabase, get_supabase, SUPABASE_REDIRECT_PATH
from django.views.decorators.http import require_GET
from invitations.invitationManager import InvitationManager

from custom_auth.factories import (
    CreateAdmin,
    CreateCitizen, 
    CreateMaintenanceCompany,
    CreateGovtBody
)

USER_CREATION_FACTORY_MAP = {
    "administrator": CreateAdmin,
    "citizen": CreateCitizen,
    "maintenance_company": CreateMaintenanceCompany,
    "govt_body":  CreateGovtBody,
}

def oauth_login(request):
    supabase = get_supabase(request)
    invitation_id = request.GET.get("invitation_id") or request.session.get("pending_invitation")

    redirect_to = f"{settings.BACKEND_URL}/auth/callback"
    
    if invitation_id:
        redirect_to += f"?invitation_id={invitation_id}"

    response = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {"redirect_to": redirect_to, "skip_browser_redirect": True}
    })

    print(response.url)
    return redirect(response.url)

def oauth_callback(request):
    
    supabase = get_supabase(request)
    code = request.GET.get('code')
    invitation_id = request.GET.get('invitation_id') or request.session.get('pending_invitation')
    is_new_user = False

    try:
        code_verifier = request.session.pop('oauth_code_verifier', None)
        supabase.auth.exchange_code_for_session({"auth_code": code, "code_verifier": code_verifier})
        session = supabase.auth.get_session()
        user = supabase.auth.get_user()

        user_id= user.user.id
        role = None

        if invitation_id:
            is_new_user = True
            print(f"Processing invitation: {invitation_id}")
            invitation_manager = InvitationManager(supabase)
                
            user_email = user.user.email if hasattr(user.user, 'email') else None
            print(f"User email: {user_email}")

            user_id= user.user.id if hasattr(user.user, 'id') else None
            print(f"Supabase user id: {user.user.id}")

            invitation = invitation_manager.get_invitation(invitation_id)
            role = invitation.get("role", "citizen")

            if not invitation_manager.mark_invitation_as_used(invitation_id, user_id):
                print("Failed to process invitation - but continuing auth flow")
        
        try:
            # Check if user already exists
            result = supabase.table("users").select("role").eq("id", user_id).maybe_single().execute()
            print(f"user role lookup: {result}")
            role = result.data.get("role") if result and result.data else None

            if role:
                print(f"Existing user detected, role: {role}")
            else:
                # New user or no role assigned
                is_new_user = True
                if not role:
                    print("No invitation found or role is empty, assigning default role 'citizen'")
                    role = "citizen"

        except Exception as fetch_err:
            print(f"Error checking user existence: {fetch_err}")
            is_new_user = True
            if not role:
                print("Fallback: assigning default role 'citizen'")
                role = "citizen"

        if is_new_user and role in USER_CREATION_FACTORY_MAP:
            factory_class = USER_CREATION_FACTORY_MAP[role]
            handler = factory_class()
            handler.create_user(user_id)

        try:
            redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={session.access_token}"
            if invitation_id:
                redirect_url += f"&invitation_id={invitation_id}"
        except Exception as e:
            redirect_url = f"{settings.FRONTEND_URL}/auth/callback?error={str(e)}"
            
        return redirect(redirect_url)
        
    except Exception as e:
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?error={str(e)}"
        return redirect(redirect_url)

def oauth_logout(request) :
    supabase = get_supabase(request)
    request.session.flush()
    django_logout(request)
    response = supabase.auth.sign_out()
    
    return JsonResponse ({
        "message": "Successfully logged out.",
        "response": response
    })

@require_GET
def get_current_user(request):
    supabase = get_supabase(request)
    user = supabase.auth.get_user()
    return JsonResponse({"user": user})

@require_GET
def get_current_user_role(request):
    user_id = request.GET.get("user_id")
    print(f"User ID: {user_id}")

    role = supabase.table("users").select("*").eq("id", user_id).single().execute()

    if role.data is None:
        return JsonResponse({"error": "Role not found"}, status=404)

    # Safe to access data
    user_role = role.data.get("role", "unknown")  # Add fallback if needed
    return JsonResponse({"role": user_role})
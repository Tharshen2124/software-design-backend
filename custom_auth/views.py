from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import JsonResponse
from clients.supabase_client import get_supabase, SUPABASE_REDIRECT_PATH
from django.views.decorators.http import require_GET
from invitations.invitationManager import InvitationManager

def oauth_login(request):
    supabase = get_supabase(request)
    invitation_id = request.GET.get("invitation_id") or request.session.get("pending_invitation")

    redirect_to = "http://127.0.0.1:8000/auth/callback"
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
    
    try:
        code_verifier = request.session.pop('oauth_code_verifier', None)
        supabase.auth.exchange_code_for_session({"auth_code": code, "code_verifier": code_verifier})
        session = supabase.auth.get_session()
        user = supabase.auth.get_user()

        if invitation_id:
            print(f"Processing invitation: {invitation_id}")
            invitation_manager = InvitationManager(supabase)
                
            user_email = user.user.email if hasattr(user.user, 'email') else None
            print(f"User email: {user_email}")

            user_id= user.user.id if hasattr(user.user, 'id') else None
            print(f"Supabase user id: {user.user.id}")

            if not invitation_manager.mark_invitation_as_used(invitation_id, user_id):
                print("Failed to process invitation - but continuing auth flow")
        
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={session.access_token}"
        if invitation_id:
            redirect_url += f"&invitation_id={invitation_id}"

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
from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import JsonResponse
from supabase_config.supabase_client import get_supabase, SUPABASE_REDIRECT_PATH
from django.views.decorators.http import require_GET

def oauth_login(request):
    supabase = get_supabase(request)

    response = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {"redirect_to": "http://localhost:8000/auth/callback"}
    })

    print(response.url)
    return redirect(response.url)

def oauth_callback(request):
    supabase = get_supabase(request)
    code = request.GET.get('code')
    
    try:
        supabase.auth.exchange_code_for_session({"auth_code": code})
        session = supabase.auth.get_session()
        
        redirect_url = f"{settings.FRONTEND_URL}/auth/callback?token={session.access_token}"
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
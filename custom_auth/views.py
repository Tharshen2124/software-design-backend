from django.shortcuts import redirect
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.http import JsonResponse
from supabase_config.supabase_client import get_supabase, SUPABASE_REDIRECT_PATH

def oauth_login(request) :
    supabase = get_supabase(request)
    redirect_url = f"{settings.BACKEND_URL}{SUPABASE_REDIRECT_PATH}"

    response = supabase.auth.sign_in_with_oauth({
        "provider" : "google",
        "options" : {"redirect_to":redirect_url}
    })

    return redirect(response.url) # this will output a url

def oauth_logout(request) :
    request.session.flush()
    django_logout(request)
    return redirect(settings.FRONTEND_URL)

def oauth_callback(request):
    supabase = get_supabase(request)
    full_url = request.build_absolute_uri()

    try:
        session = supabase.auth.get_session()
        user = supabase.auth.get_user()
        return redirect(f"{settings.BACKEND_URL}/hehe?token={session.access_token}")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

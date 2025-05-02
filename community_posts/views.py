from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from supabase_config.supabase_client import supabase

@csrf_exempt
def posts_list_create(request):
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'user_id': request.POST.get('user_id')
        }
        res = supabase.table('posts').insert(data).execute()
        return JsonResponse(res.data[0], status=201)
    
    res = supabase.table('posts').select('*').execute()
    return JsonResponse({'posts': res.data})
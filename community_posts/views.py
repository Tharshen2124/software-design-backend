from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from supabase_config.supabase_client import supabase
from cloudinary_client import CloudinaryClient

@csrf_exempt
def posts_list_create(request):
    if request.method == 'POST':
        image = request.FILES.get('image_url')
        if image:
            cloudinary_client = CloudinaryClient()
            response = cloudinary_client.upload(image)
        else:
            return JsonResponse({"error": "No image provided"}, status=400)

        data = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'user_id': request.POST.get('user_id'),
            'image_url': response['secure_url']
        }

        res = supabase.table('posts').insert(data).execute()
        return JsonResponse(res.data[0], status=201)
    
    res = supabase.table('posts').select('*, user_id:users(*)').execute()
    return JsonResponse({'posts': res.data})

@csrf_exempt
def post_detail(request, post_id):
    if request.method == 'GET':
        res = supabase.table('posts').select('*').eq('id', post_id).execute()
        if not res.data:
            raise Http404("Post not found")
        return JsonResponse(res.data[0])
    
    elif request.method == 'DELETE':
        supabase.table('posts').delete().eq('id', post_id).execute()
        return JsonResponse({'status': 'deleted'}, status=204)
    
@csrf_exempt
def post_comments(request, post_id):
    if request.method == 'POST':
        data = {
            'post_id': post_id,
            'user_id': request.POST.get('user_id'),  # Now matches posts_list_create
            'comment_description': request.POST.get('comment')
        }
        res = supabase.table('comments').insert(data).execute()
        return JsonResponse(res.data[0], status=201)
    
    res = supabase.table('comments').select('*').eq('post_id', post_id).execute()
    return JsonResponse({'comments': res.data})
    
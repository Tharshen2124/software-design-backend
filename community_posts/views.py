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
    
    
    res = supabase.table('posts').select('*, users(profile_picture, full_name)').execute()
    return JsonResponse({'posts': res.data})

@csrf_exempt
def post_detail(request, post_id):
    if request.method == 'GET':
        # Simple post retrieval without joins
        post_res = supabase.table('posts').select('*').eq('id', post_id).execute()
        
        if not post_res.data:
            raise Http404("Post not found")
        
        # Get comments separately
        comments_res = supabase.table('comments').select('*').eq('post_id', post_id).execute()
        
        # Combine the data
        result = post_res.data[0]
        result['comments'] = comments_res.data
            
        return JsonResponse(result)
    
    elif request.method == 'DELETE':
        supabase.table('posts').delete().eq('id', post_id).execute()
        return JsonResponse({'status': 'deleted'}, status=204)
    
@csrf_exempt
def post_comments(request, post_id):
    if request.method == 'POST':
        data = {
            'post_id': post_id,
            'user_id': request.POST.get('user_id'),
            'comment_description': request.POST.get('comment')
        }
        res = supabase.table('comments').insert(data).execute()
        return JsonResponse(res.data[0], status=201)
    
    # Simple comment retrieval 
    comments_res = supabase.table('comments').select('*').eq('post_id', post_id).execute()
    return JsonResponse({'comments': comments_res.data})
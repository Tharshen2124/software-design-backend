from django.http import JsonResponse
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
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
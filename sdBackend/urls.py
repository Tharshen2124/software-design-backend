from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('custom_auth.urls')),
    path("posts/", include("community_posts.urls")), 
    path("complaints/", include("complaints.urls.complaints_urls")),
    path("maintenance/", include("complaints.urls.maintenance_urls")),
    path('invitation/', include('invitations.urls')),
    path('', include('usercomponents.urls')),
]

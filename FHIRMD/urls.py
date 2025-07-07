from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Removed path('accounts/', include('allauth.urls')),
    
    # Your existing frontend URLs
    path('', include('frontend.urls')),
]
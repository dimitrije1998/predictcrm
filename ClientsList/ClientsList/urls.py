from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('list.urls')),  # uključi urls aplikacije 'list' za root URL
]

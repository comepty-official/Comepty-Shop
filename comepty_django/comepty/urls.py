import os  # <-- ADD THIS
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse  # <-- ADD THIS
from .views import custom_page_not_found, custom_server_error

def superuser_required(view_func):
    decorated_view = user_passes_test(lambda u: u.is_superuser, login_url='/users/login/')(view_func)
    return decorated_view

def discord_verification(request):
    file_path = os.path.join(settings.BASE_DIR, '.well-known', 'discord')
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return HttpResponse(content, content_type="text/plain")
    else:
        return HttpResponse("Verification file not found", status=404)

admin.site.login = superuser_required(admin.site.login)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path('ai/', include('ai_section.urls')),
    path('pages/', include('pages.urls')),
    path('.well-known/discord', discord_verification),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_page_not_found
handler500 = custom_server_error

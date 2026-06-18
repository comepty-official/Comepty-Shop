from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import user_passes_test
from .views import custom_page_not_found, custom_server_error

def superuser_required(view_func):
    decorated_view = user_passes_test(lambda u: u.is_superuser, login_url='/users/login/')(view_func)
    return decorated_view

admin.site.login = superuser_required(admin.site.login)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include('products.urls')),
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path('ai/', include('ai_section.urls')),
    path('pages/', include('pages.urls')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# Override the default error pages
handler404 = custom_page_not_found
handler500 = custom_server_error
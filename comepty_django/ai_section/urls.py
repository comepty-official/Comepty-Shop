from django.urls import path
from . import views

urlpatterns = [
    path('', views.ai_chat, name='ai_chat'),
    path('ask/', views.ai_ask, name='ai_ask'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('start/<str:username>/', views.start_conversation, name='start_conversation'),
    path('<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('<int:pk>/poll/', views.poll_messages, name='poll_messages'),
]

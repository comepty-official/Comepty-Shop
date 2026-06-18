from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('<int:pk>/save/', views.toggle_save, name='toggle_save'),
    path('<int:pk>/track-click/', views.track_click, name='track_click'),
    path('<int:pk>/report/', views.report_product, name='report_product'),
    path('<int:pk>/add-user-video/', views.add_user_video, name='add_user_video'),
    path('user-video/<int:pk>/delete/', views.delete_user_video, name='delete_user_video'),
    path('feed/', views.video_feed, name='video_feed'),
    path('my-products/', views.my_products, name='my_products'),
    path('saved/', views.saved_products, name='saved_products'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
]

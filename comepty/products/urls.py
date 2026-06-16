from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='list'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('my-products/', views.my_products, name='my_products'),
    path('saved/', views.saved_products, name='saved'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.ProductUpdateView.as_view(), name='edit'),
    path('<slug:slug>/like/', views.toggle_like, name='like'),
    path('<slug:slug>/save/', views.toggle_save, name='save'),
    path('<slug:slug>/click/', views.affiliate_click, name='affiliate_click'),
    path('<slug:slug>/comment/', views.add_comment, name='comment'),
]

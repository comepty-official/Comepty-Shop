from django.shortcuts import render
from django.db.models import Q
from products.models import Product, Category


def home(request):
    featured = Product.objects.filter(is_approved=True, is_featured=True, owner__profile__is_deleted=False).order_by('-created_at')[:6]
    latest = Product.objects.filter(is_approved=True, owner__profile__is_deleted=False).order_by('-created_at')[:12]
    trending = Product.objects.filter(is_approved=True, owner__profile__is_deleted=False).order_by('-click_count')[:8]
    video_products = Product.objects.filter(is_approved=True, owner__profile__is_deleted=False, videos__isnull=False).distinct().order_by('-created_at')[:6]
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'featured': featured,
        'latest': latest,
        'trending': trending,
        'video_products': video_products,
        'categories': categories,
    })


def search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    products = Product.objects.filter(is_approved=True, owner__profile__is_deleted=False)
    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    if category_id:
        products = products.filter(category__id=category_id)
    products = products.order_by('-created_at')
    return render(request, 'core/search.html', {
        'products': products,
        'query': query,
        'selected_category': category_id,
    })

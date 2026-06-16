from django.shortcuts import render
from django.db.models import Q
from products.models import Product, Category


def home(request):
    featured = Product.objects.filter(status='approved').order_by('-like_count')[:8]
    newest = Product.objects.filter(status='approved').order_by('-created_at')[:8]
    trending = Product.objects.filter(status='approved').order_by('-view_count')[:6]
    categories = Category.objects.all()
    has_video = Product.objects.filter(status='approved').exclude(youtube_url='').order_by('-created_at')[:4]
    return render(request, 'core/home.html', {
        'featured': featured,
        'newest': newest,
        'trending': trending,
        'categories': categories,
        'has_video': has_video,
    })


def search(request):
    q = request.GET.get('q', '')
    products = Product.objects.none()
    if q:
        products = Product.objects.filter(
            status='approved'
        ).filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(creator__username__icontains=q) |
            Q(category__name__icontains=q)
        ).distinct()
    return render(request, 'core/search.html', {'products': products, 'q': q})

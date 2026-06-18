from products.models import Category


def site_context(request):
    categories = Category.objects.all()
    return {
        'site_name': 'Comepty',
        'categories': categories,
    }

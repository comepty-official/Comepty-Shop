from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from .models import Product, Category, ProductImage, Like, SavedProduct, Comment, AffiliateClick
from .forms import ProductForm, ProductImageFormSet, CommentForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(status='approved').select_related('creator', 'category').prefetch_related('images')
        q = self.request.GET.get('q')
        category = self.request.GET.get('category')
        sort = self.request.GET.get('sort', 'newest')

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category__slug=category)

        if sort == 'popular':
            qs = qs.order_by('-view_count')
        elif sort == 'trending':
            qs = qs.order_by('-like_count')
        elif sort == 'oldest':
            qs = qs.order_by('created_at')
        else:
            qs = qs.order_by('-created_at')

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_q'] = self.request.GET.get('q', '')
        ctx['current_category'] = self.request.GET.get('category', '')
        ctx['current_sort'] = self.request.GET.get('sort', 'newest')
        return ctx


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(status='approved')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Increment view count
        Product.objects.filter(pk=self.object.pk).update(view_count=F('view_count') + 1)
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        ctx['comments'] = self.object.comments.select_related('user').all()[:20]
        ctx['related'] = Product.objects.filter(
            category=self.object.category, status='approved'
        ).exclude(pk=self.object.pk)[:6]
        if self.request.user.is_authenticated:
            ctx['is_liked'] = self.object.is_liked_by(self.request.user)
            ctx['is_saved'] = self.object.is_saved_by(self.request.user)
        return ctx


class FeedView(ListView):
    """TikTok-style vertical video feed"""
    model = Product
    template_name = 'products/feed.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(
            status='approved'
        ).exclude(
            youtube_url='', video_file=''
        ).select_related('creator', 'category').prefetch_related('images').order_by('-created_at')


class CategoryView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Product.objects.filter(category=self.category, status='approved').select_related('creator').prefetch_related('images')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_category_obj'] = self.category
        return ctx


@method_decorator(login_required, name='dispatch')
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES)
        else:
            ctx['image_formset'] = ProductImageFormSet()
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        image_formset = ctx['image_formset']
        form.instance.creator = self.request.user
        form.instance.status = 'pending'

        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, '🎉 Product submitted! It will go live after admin approval.')
            return redirect('products:detail', slug=self.object.slug)
        else:
            return self.form_invalid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'

    def get_queryset(self):
        return Product.objects.filter(creator=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.POST:
            ctx['image_formset'] = ProductImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            ctx['image_formset'] = ProductImageFormSet(instance=self.object)
        ctx['is_edit'] = True
        return ctx

    def form_valid(self, form):
        ctx = self.get_context_data()
        image_formset = ctx['image_formset']
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, 'Product updated successfully!')
            return redirect('products:detail', slug=self.object.slug)
        return self.form_invalid(form)


# --- AJAX / Action Views ---

@login_required
def toggle_like(request, slug):
    product = get_object_or_404(Product, slug=slug, status='approved')
    like, created = Like.objects.get_or_create(user=request.user, product=product)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    count = product.likes.count()
    Product.objects.filter(pk=product.pk).update(like_count=count)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': count})
    return redirect('products:detail', slug=slug)


@login_required
def toggle_save(request, slug):
    product = get_object_or_404(Product, slug=slug, status='approved')
    save, created = SavedProduct.objects.get_or_create(user=request.user, product=product)
    if not created:
        save.delete()
        saved = False
    else:
        saved = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'saved': saved})
    return redirect('products:detail', slug=slug)


def affiliate_click(request, slug):
    product = get_object_or_404(Product, slug=slug, status='approved')
    AffiliateClick.objects.create(
        product=product,
        user=request.user if request.user.is_authenticated else None,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referrer=request.META.get('HTTP_REFERER', ''),
    )
    Product.objects.filter(pk=product.pk).update(click_count=F('click_count') + 1)
    return HttpResponseRedirect(product.affiliate_link)


@login_required
def add_comment(request, slug):
    product = get_object_or_404(Product, slug=slug, status='approved')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            messages.success(request, 'Comment added!')
    return redirect('products:detail', slug=slug)


@login_required
def my_products(request):
    products = Product.objects.filter(creator=request.user).order_by('-created_at')
    return render(request, 'products/my_products.html', {'products': products})


@login_required
def saved_products(request):
    saves = SavedProduct.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    products = [s.product for s in saves]
    return render(request, 'products/saved.html', {'products': products})

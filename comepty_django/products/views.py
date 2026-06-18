from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from .models import (Product, ProductImage, ProductVideo, Like, Comment,
                     SavedProduct, ProductClick, Report, Tag, UserProductVideo, AdminBlogPost)
from .forms import ProductForm, ProductImageForm, ProductVideoForm, CommentForm, ReportForm, UserProductVideoForm


def product_list(request):
    products = Product.objects.filter(is_approved=True, owner__profile__is_deleted=False)
    category = request.GET.get('category')
    sort = request.GET.get('sort', 'newest')
    if category:
        products = products.filter(category__slug=category)
    if sort == 'popular':
        products = products.order_by('-click_count')
    elif sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'products/list.html', {'products': products, 'sort': sort})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if not product.is_approved and not (
        request.user.is_authenticated and (
            request.user == product.owner or request.user.is_staff or request.user.is_superuser
        )
    ):
        raise Http404('No Product matches the given query.')

    if product.owner.profile.is_deleted:
        messages.error(request, 'This product is no longer available.')
        return redirect('home')

    product.view_count += 1
    product.save(update_fields=['view_count'])

    user_liked = False
    user_saved = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, product=product).exists()
        user_saved = SavedProduct.objects.filter(user=request.user, product=product).exists()

    comments = product.comments.select_related('user').order_by('-created_at')
    comment_form = CommentForm()
    report_form = ReportForm()
    user_video_form = UserProductVideoForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, 'Please log in to comment.')
            return redirect('login')
        action = request.POST.get('action')
        if action == 'comment':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                c = comment_form.save(commit=False)
                c.user = request.user
                c.product = product
                c.save()
                messages.success(request, 'Comment posted!')
                return redirect('product_detail', pk=pk)
        elif action == 'report':
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                r = report_form.save(commit=False)
                r.reporter = request.user
                r.product = product
                r.save()
                messages.success(request, 'Report submitted. Thank you!')
                return redirect('product_detail', pk=pk)

    approved_user_videos = product.user_videos.filter(is_approved=True).select_related('user')

    return render(request, 'products/detail.html', {
        'product': product,
        'user_liked': user_liked,
        'user_saved': user_saved,
        'comments': comments,
        'comment_form': comment_form,
        'report_form': report_form,
        'user_video_form': user_video_form,
        'approved_user_videos': approved_user_videos,
    })


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.status = 'pending'
            product.is_approved = False
            product.save()
            form.save_m2m()

            new_tags_raw = form.cleaned_data.get('new_tags', '')
            if new_tags_raw:
                for tag_name in new_tags_raw.split(','):
                    tag_name = tag_name.strip().lower()
                    if tag_name:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        product.tags.add(tag)

            images = request.FILES.getlist('images')
            for i, img in enumerate(images):
                ProductImage.objects.create(product=product, image=img, order=i)

            videos = request.FILES.getlist('videos')
            captions = request.POST.getlist('video_captions')
            for i, vid in enumerate(videos):
                cap = captions[i] if i < len(captions) else ''
                ProductVideo.objects.create(product=product, video=vid, caption=cap, order=i)

            messages.success(request, 'Product submitted for approval! An admin will review it shortly.')
            return redirect('my_products')
    else:
        form = ProductForm()
    return render(request, 'products/create.html', {'form': form})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            p = form.save(commit=False)
            p.status = 'pending'
            p.is_approved = False
            p.save()
            form.save_m2m()

            new_tags_raw = form.cleaned_data.get('new_tags', '')
            if new_tags_raw:
                for tag_name in new_tags_raw.split(','):
                    tag_name = tag_name.strip().lower()
                    if tag_name:
                        tag, _ = Tag.objects.get_or_create(name=tag_name)
                        product.tags.add(tag)

            new_images = request.FILES.getlist('images')
            existing_count = product.images.count()
            for i, img in enumerate(new_images):
                ProductImage.objects.create(product=product, image=img, order=existing_count + i)

            new_videos = request.FILES.getlist('videos')
            captions = request.POST.getlist('video_captions')
            existing_vid_count = product.videos.count()
            for i, vid in enumerate(new_videos):
                cap = captions[i] if i < len(captions) else ''
                ProductVideo.objects.create(product=product, video=vid, caption=cap, order=existing_vid_count + i)

            messages.success(request, 'Product updated and resubmitted for approval.')
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/create.html', {'form': form, 'product': product, 'edit': True})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted.')
    return redirect('my_products')


@login_required
@require_POST
def toggle_like(request, pk):
    product = get_object_or_404(Product, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, product=product)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({'liked': liked, 'count': product.get_like_count()})


@login_required
@require_POST
def toggle_save(request, pk):
    product = get_object_or_404(Product, pk=pk)
    saved, created = SavedProduct.objects.get_or_create(user=request.user, product=product)
    if not created:
        saved.delete()
        is_saved = False
    else:
        is_saved = True
    return JsonResponse({'saved': is_saved})


def track_click(request, pk):
    product = get_object_or_404(Product, pk=pk)
    ip = request.META.get('REMOTE_ADDR')
    ProductClick.objects.create(
        product=product,
        user=request.user if request.user.is_authenticated else None,
        ip_address=ip
    )
    product.click_count += 1
    product.save(update_fields=['click_count'])
    if product.affiliate_link:
        return JsonResponse({'redirect': product.affiliate_link, 'count': product.click_count})
    return JsonResponse({'redirect': None, 'count': product.click_count})


@login_required
def report_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.reporter = request.user
            r.product = product
            r.save()
            messages.success(request, 'Report submitted. Thank you!')
    return redirect('product_detail', pk=pk)


@login_required
def add_user_video(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = UserProductVideoForm(request.POST, request.FILES)
        if form.is_valid():
            uv = form.save(commit=False)
            uv.product = product
            uv.user = request.user
            uv.save()
            messages.success(request, 'Your video has been posted!')
    return redirect('product_detail', pk=pk)


@login_required
def delete_user_video(request, pk):
    uv = get_object_or_404(UserProductVideo, pk=pk)
    if request.user == uv.user or request.user.is_staff:
        uv.delete()
        messages.success(request, 'Video deleted.')
    return redirect('product_detail', pk=uv.product.pk)


def video_feed(request):
    # Build a product-based feed: one (latest) video per approved product.
    products = Product.objects.filter(
        is_approved=True,
        owner__profile__is_deleted=False,
        videos__isnull=False
    ).distinct().order_by('-created_at')

    videos = []
    for p in products:
        vid = p.videos.filter().order_by('-created_at').select_related('product').first()
        if vid:
            videos.append(vid)

    return render(request, 'products/feed.html', {'videos': videos})


@login_required
def my_products(request):
    products = Product.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'products/my_products.html', {'products': products})


@login_required
def saved_products(request):
    saved = SavedProduct.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    return render(request, 'products/saved.html', {'saved': saved})


def blog_list(request):
    posts = AdminBlogPost.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'products/blog_list.html', {'posts': posts})


def blog_detail(request, pk):
    post = get_object_or_404(AdminBlogPost, pk=pk, is_published=True)
    return render(request, 'products/blog_detail.html', {'post': post})

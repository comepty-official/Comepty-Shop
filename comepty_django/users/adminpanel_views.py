from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from products.models import Product, Report, AdminBlogPost
from .models import Profile


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_superuser, login_url='/users/login/')(view_func)


# ──────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────
@superuser_required
def panel_dashboard(request):
    ctx = {
        'pending_count': Product.objects.filter(status='pending').count(),
        'approved_count': Product.objects.filter(status='approved').count(),
        'rejected_count': Product.objects.filter(status='rejected').count(),
        'total_users': User.objects.filter(profile__is_deleted=False).count(),
        'deleted_users': User.objects.filter(profile__is_deleted=True).count(),
        'open_reports': Report.objects.filter(resolved=False).count(),
        'total_reports': Report.objects.count(),
        'unpublished_posts': AdminBlogPost.objects.filter(is_published=False).count(),
        'recent_products': Product.objects.order_by('-created_at')[:5],
        'recent_users': User.objects.order_by('-date_joined')[:5],
    }
    return render(request, 'adminpanel/dashboard.html', ctx)


# ──────────────────────────────────────────────
# PRODUCTS — Pending
# ──────────────────────────────────────────────
@superuser_required
def panel_pending_products(request):
    products = Product.objects.filter(status='pending').select_related('owner', 'category').order_by('-created_at')
    return render(request, 'adminpanel/pending_products.html', {'products': products})


@superuser_required
@require_POST
def panel_approve_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'approved'
    product.save()
    messages.success(request, f'"{product.title}" approved and is now live.')
    return redirect(request.POST.get('next', 'panel_pending_products'))


@superuser_required
@require_POST
def panel_reject_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'rejected'
    product.save()
    messages.warning(request, f'"{product.title}" has been rejected.')
    return redirect(request.POST.get('next', 'panel_pending_products'))


# ──────────────────────────────────────────────
# PRODUCTS — All
# ──────────────────────────────────────────────
@superuser_required
def panel_all_products(request):
    status_filter = request.GET.get('status', '')
    products = Product.objects.select_related('owner', 'category').order_by('-created_at')
    if status_filter:
        products = products.filter(status=status_filter)
    return render(request, 'adminpanel/all_products.html', {'products': products, 'status_filter': status_filter})


@superuser_required
@require_POST
def panel_feature_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_featured = not product.is_featured
    product.save(update_fields=['is_featured'])
    label = 'featured' if product.is_featured else 'unfeatured'
    messages.success(request, f'"{product.title}" is now {label}.')
    return redirect('panel_all_products')


@superuser_required
@require_POST
def panel_delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = product.title
    product.delete()
    messages.success(request, f'"{title}" has been deleted.')
    return redirect('panel_all_products')


# ──────────────────────────────────────────────
# USERS
# ──────────────────────────────────────────────
@superuser_required
def panel_users(request):
    search = request.GET.get('q', '')
    show = request.GET.get('show', 'active')
    users = User.objects.select_related('profile').order_by('-date_joined')
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    if show == 'deleted':
        users = users.filter(profile__is_deleted=True)
    else:
        users = users.filter(profile__is_deleted=False)
    return render(request, 'adminpanel/users.html', {'users': users, 'search': search, 'show': show})


@superuser_required
@require_POST
def panel_deactivate_user(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target.is_superuser:
        messages.error(request, 'Cannot deactivate a superuser.')
        return redirect('panel_users')
    profile, _ = Profile.objects.get_or_create(user=target)
    profile.is_deleted = True
    profile.deleted_at = timezone.now()
    profile.save()
    messages.success(request, f'User "{target.username}" deactivated.')
    return redirect('panel_users')


@superuser_required
@require_POST
def panel_restore_user(request, pk):
    target = get_object_or_404(User, pk=pk)
    profile, _ = Profile.objects.get_or_create(user=target)
    profile.is_deleted = False
    profile.deleted_at = None
    profile.save()
    messages.success(request, f'User "{target.username}" restored.')
    return redirect('panel_users')


@superuser_required
@require_POST
def panel_delete_user(request, pk):
    target = get_object_or_404(User, pk=pk)
    if target.is_superuser:
        messages.error(request, 'Cannot delete a superuser.')
        return redirect('panel_users')
    username = target.username
    target.delete()
    messages.success(request, f'User "{username}" permanently deleted.')
    return redirect('panel_users')


@superuser_required
@require_POST
def panel_make_staff(request, pk):
    target = get_object_or_404(User, pk=pk)
    target.is_staff = not target.is_staff
    target.save(update_fields=['is_staff'])
    label = 'promoted to staff' if target.is_staff else 'removed from staff'
    messages.success(request, f'"{target.username}" {label}.')
    return redirect('panel_users')


# ──────────────────────────────────────────────
# REPORTS
# ──────────────────────────────────────────────
@superuser_required
def panel_reports(request):
    show = request.GET.get('show', 'open')
    reports = Report.objects.select_related('reporter', 'product').order_by('-created_at')
    if show == 'resolved':
        reports = reports.filter(resolved=True)
    else:
        reports = reports.filter(resolved=False)
    return render(request, 'adminpanel/reports.html', {'reports': reports, 'show': show})


@superuser_required
@require_POST
def panel_resolve_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.resolved = True
    report.save(update_fields=['resolved'])
    messages.success(request, 'Report marked as resolved.')
    return redirect('panel_reports')


@superuser_required
@require_POST
def panel_delete_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    report.delete()
    messages.success(request, 'Report deleted.')
    return redirect('panel_reports')


# ──────────────────────────────────────────────
# BLOG
# ──────────────────────────────────────────────
@superuser_required
def panel_blog(request):
    posts = AdminBlogPost.objects.select_related('author').order_by('-created_at')
    return render(request, 'adminpanel/blog.html', {'posts': posts})


@superuser_required
def panel_blog_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        publish = request.POST.get('publish') == '1'
        if title and content:
            AdminBlogPost.objects.create(
                author=request.user,
                title=title,
                content=content,
                is_published=publish,
            )
            messages.success(request, 'Blog post created.')
            return redirect('panel_blog')
        else:
            messages.error(request, 'Title and content are required.')
    return render(request, 'adminpanel/blog_form.html', {'post': None})


@superuser_required
def panel_blog_edit(request, pk):
    post = get_object_or_404(AdminBlogPost, pk=pk)
    if request.method == 'POST':
        post.title = request.POST.get('title', post.title).strip()
        post.content = request.POST.get('content', post.content).strip()
        post.is_published = request.POST.get('publish') == '1'
        post.save()
        messages.success(request, 'Blog post updated.')
        return redirect('panel_blog')
    return render(request, 'adminpanel/blog_form.html', {'post': post})


@superuser_required
@require_POST
def panel_blog_toggle_publish(request, pk):
    post = get_object_or_404(AdminBlogPost, pk=pk)
    post.is_published = not post.is_published
    post.save(update_fields=['is_published'])
    label = 'published' if post.is_published else 'unpublished'
    messages.success(request, f'"{post.title}" {label}.')
    return redirect('panel_blog')


@superuser_required
@require_POST
def panel_blog_delete(request, pk):
    post = get_object_or_404(AdminBlogPost, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, f'"{title}" deleted.')
    return redirect('panel_blog')

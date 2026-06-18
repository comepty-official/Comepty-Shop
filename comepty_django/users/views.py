from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import RegisterForm, LoginForm, ProfileEditForm, UserEditForm
from .models import Profile
from products.models import Product


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            existing = User.objects.filter(email=email).first()
            if existing:
                try:
                    send_mail(
                        subject='Someone tried to register with your email - Comepty',
                        message=(
                            f'Hi {existing.username},\n\n'
                            'Someone tried to create a new account on Comepty using your email address. '
                            'If this was you and you forgot your password, you can reset it at any time.\n\n'
                            'If this was NOT you, please ignore this email.\n\n'
                            '— The Comepty Team'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=True,
                    )
                except Exception:
                    pass
                messages.error(request, 'This email is already registered. We sent a notice to that address.')
            else:
                user = form.save()
                Profile.objects.get_or_create(user=user)
                login(request, user)
                messages.success(request, f'Welcome to Comepty, {user.username}!')
                return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if hasattr(user, 'profile') and user.profile.is_deleted:
                messages.error(request, 'This account has been deactivated.')
                return render(request, 'users/login.html', {'form': form})
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', '/')
            if 'admin' in next_url and not user.is_superuser:
                return redirect('home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm(request)
    return render(request, 'users/login.html', {'form': form})


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    if hasattr(profile_user, 'profile') and profile_user.profile.is_deleted:
        messages.error(request, 'This account is no longer active.')
        return redirect('home')
    products = Product.objects.filter(owner=profile_user, is_approved=True).order_by('-created_at')
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'products': products,
    })


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=request.user.username)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=profile)
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def delete_account(request):
    if request.method == 'POST':
        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.is_deleted = True
        profile.deleted_at = timezone.now()
        profile.save()
        logout(request)
        messages.success(request, 'Your account has been deactivated. Your data is retained per our privacy policy.')
        return redirect('home')
    return render(request, 'users/delete_account.html')


def users_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    users = User.objects.exclude(id=request.user.id).filter(profile__is_deleted=False).select_related('profile')
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        # Search by username or first/last name
        from django.db.models import Q
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    return render(request, 'users/users_list.html', {'users': users, 'search_query': search_query})

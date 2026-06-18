from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import adminpanel_views as apv

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('users-list/', views.users_list, name='users_list'),

    # ── Admin Panel ──────────────────────────────────────────────
    path('panel/', apv.panel_dashboard, name='panel_dashboard'),

    path('panel/products/pending/', apv.panel_pending_products, name='panel_pending_products'),
    path('panel/products/<int:pk>/approve/', apv.panel_approve_product, name='panel_approve_product'),
    path('panel/products/<int:pk>/reject/', apv.panel_reject_product, name='panel_reject_product'),

    path('panel/products/all/', apv.panel_all_products, name='panel_all_products'),
    path('panel/products/<int:pk>/feature/', apv.panel_feature_product, name='panel_feature_product'),
    path('panel/products/<int:pk>/delete/', apv.panel_delete_product, name='panel_delete_product'),

    path('panel/users/', apv.panel_users, name='panel_users'),
    path('panel/users/<int:pk>/deactivate/', apv.panel_deactivate_user, name='panel_deactivate_user'),
    path('panel/users/<int:pk>/restore/', apv.panel_restore_user, name='panel_restore_user'),
    path('panel/users/<int:pk>/delete/', apv.panel_delete_user, name='panel_delete_user'),
    path('panel/users/<int:pk>/staff/', apv.panel_make_staff, name='panel_make_staff'),

    path('panel/reports/', apv.panel_reports, name='panel_reports'),
    path('panel/reports/<int:pk>/resolve/', apv.panel_resolve_report, name='panel_resolve_report'),
    path('panel/reports/<int:pk>/delete/', apv.panel_delete_report, name='panel_delete_report'),

    path('panel/blog/', apv.panel_blog, name='panel_blog'),
    path('panel/blog/create/', apv.panel_blog_create, name='panel_blog_create'),
    path('panel/blog/<int:pk>/edit/', apv.panel_blog_edit, name='panel_blog_edit'),
    path('panel/blog/<int:pk>/publish/', apv.panel_blog_toggle_publish, name='panel_blog_toggle_publish'),
    path('panel/blog/<int:pk>/delete/', apv.panel_blog_delete, name='panel_blog_delete'),
]

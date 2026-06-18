from django.contrib import admin
from django.utils.html import format_html
from .models import (Product, ProductImage, ProductVideo, Category, Tag,
                     Like, Comment, SavedProduct, Report, AdminBlogPost,
                     UserProductVideo, ProductClick)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'category', 'status', 'is_featured', 'click_count', 'created_at']
    list_filter = ['status', 'is_featured', 'category']
    search_fields = ['title', 'owner__username']
    actions = ['approve_products', 'reject_products', 'feature_products', 'unfeature_products']
    inlines = [ProductImageInline, ProductVideoInline]

    def approve_products(self, request, queryset):
        queryset.update(status='approved', is_approved=True)
        self.message_user(request, f'{queryset.count()} product(s) approved.')
    approve_products.short_description = 'Approve selected products'

    def reject_products(self, request, queryset):
        queryset.update(status='rejected', is_approved=False)
        self.message_user(request, f'{queryset.count()} product(s) rejected.')
    reject_products.short_description = 'Reject selected products'

    def feature_products(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} product(s) featured on homepage.')
    feature_products.short_description = 'Feature on homepage'

    def unfeature_products(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} product(s) removed from featured.')
    unfeature_products.short_description = 'Remove from featured'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text', 'created_at']
    actions = ['delete_selected']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'product', 'reason', 'resolved', 'created_at']
    list_filter = ['reason', 'resolved']
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(resolved=True)
    mark_resolved.short_description = 'Mark as resolved'


@admin.register(UserProductVideo)
class UserProductVideoAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'is_approved', 'created_at']
    actions = ['approve_videos', 'delete_selected']

    def approve_videos(self, request, queryset):
        queryset.update(is_approved=True)
    approve_videos.short_description = 'Approve selected videos'


@admin.register(AdminBlogPost)
class AdminBlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published']


admin.site.register(Like)
admin.site.register(SavedProduct)
admin.site.register(ProductClick)

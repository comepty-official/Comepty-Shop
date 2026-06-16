from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductImage, Category, Like, SavedProduct, Comment, AffiliateClick


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ['preview']

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return '-'
    preview.short_description = 'Preview'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'category', 'status', 'view_count', 'click_count', 'like_count', 'created_at', 'thumbnail_preview']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'description', 'creator__username']
    list_editable = ['status']
    readonly_fields = ['view_count', 'click_count', 'like_count', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('title',)}
    actions = ['approve_products', 'reject_products']

    def thumbnail_preview(self, obj):
        img = obj.primary_image
        if img:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;" />', img.url)
        return '—'
    thumbnail_preview.short_description = 'Image'

    def approve_products(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'{queryset.count()} products approved.')
    approve_products.short_description = '✅ Approve selected products'

    def reject_products(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'{queryset.count()} products rejected.')
    reject_products.short_description = '❌ Reject selected products'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'color', 'product_count']
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'text', 'created_at']
    list_filter = ['created_at']


@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'ip_address', 'clicked_at']
    list_filter = ['clicked_at']
    readonly_fields = ['product', 'user', 'ip_address', 'user_agent', 'clicked_at', 'referrer']


admin.site.register(Like)
admin.site.register(SavedProduct)

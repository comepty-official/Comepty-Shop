from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Category(models.Model):
    ICONS = {
        'tech': '💻',
        'software': '⚙️',
        'fashion': '👗',
        'business': '💼',
        'gaming': '🎮',
        'courses': '📚',
        'health': '🏥',
        'travel': '✈️',
        'food': '🍔',
        'beauty': '💄',
    }

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=7, default='#6366f1')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.icon:
            self.icon = self.ICONS.get(self.slug, '🏷️')
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        return self.products.filter(status='approved').count()


class Product(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('draft', 'Draft'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    affiliate_link = models.URLField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Stats
    view_count = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)

    # Video
    youtube_url = models.URLField(blank=True, help_text='YouTube or Vimeo URL')
    video_file = models.FileField(upload_to='videos/', blank=True)

    # Thumbnail (main display image)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def get_affiliate_url(self):
        return reverse('products:affiliate_click', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        img = self.images.first()
        return img.image if img else self.thumbnail or None

    @property
    def embed_url(self):
        """Convert YouTube URL to embed format"""
        url = self.youtube_url
        if not url:
            return None
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        if 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[-1].split('?')[0]
            return f'https://player.vimeo.com/video/{video_id}'
        return url

    @property
    def formatted_price(self):
        if self.price:
            return f'${self.price:,.2f}'
        return 'Free'

    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

    def is_saved_by(self, user):
        if user.is_authenticated:
            return self.saves.filter(user=user).exists()
        return False


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'{self.product.title} - Image {self.order}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user.username} likes {self.product.title}'


class SavedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saves')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} on {self.product.title}'


class AffiliateClick(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='affiliate_clicks')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)
    referrer = models.URLField(blank=True)

    def __str__(self):
        return f'Click on {self.product.title} at {self.clicked_at}'

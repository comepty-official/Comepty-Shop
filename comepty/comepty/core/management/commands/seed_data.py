"""
Management command to seed the database with initial categories.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from products.models import Category


class Command(BaseCommand):
    help = 'Seed the database with default categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Tech', 'slug': 'tech', 'icon': '💻', 'color': '#6366f1', 'description': 'Gadgets, electronics, and tech accessories'},
            {'name': 'Software', 'slug': 'software', 'icon': '⚙️', 'color': '#8B5CF6', 'description': 'Apps, SaaS tools, and digital software'},
            {'name': 'Fashion', 'slug': 'fashion', 'icon': '👗', 'color': '#EC4899', 'description': 'Clothing, accessories, and style'},
            {'name': 'Business', 'slug': 'business', 'icon': '💼', 'color': '#0EA5E9', 'description': 'Business tools, services, and resources'},
            {'name': 'Gaming', 'slug': 'gaming', 'icon': '🎮', 'color': '#10B981', 'description': 'Games, controllers, and gaming gear'},
            {'name': 'Courses', 'slug': 'courses', 'icon': '📚', 'color': '#F59E0B', 'description': 'Online courses, ebooks, and learning resources'},
            {'name': 'Health', 'slug': 'health', 'icon': '🏥', 'color': '#EF4444', 'description': 'Health products, supplements, and wellness'},
            {'name': 'Beauty', 'slug': 'beauty', 'icon': '💄', 'color': '#F43F5E', 'description': 'Skincare, makeup, and beauty products'},
            {'name': 'Travel', 'slug': 'travel', 'icon': '✈️', 'color': '#06B6D4', 'description': 'Travel gear, bookings, and accessories'},
            {'name': 'Food', 'slug': 'food', 'icon': '🍔', 'color': '#84CC16', 'description': 'Food products, supplements, and kitchen tools'},
        ]

        created_count = 0
        for cat_data in categories:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ Created: {cat.icon} {cat.name}'))
            else:
                self.stdout.write(f'  — Already exists: {cat.icon} {cat.name}')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Done! Created {created_count} new categories.'))
        self.stdout.write('\nNext steps:')
        self.stdout.write('  1. python manage.py createsuperuser')
        self.stdout.write('  2. python manage.py runserver')
        self.stdout.write('  3. Visit http://127.0.0.1:8000/admin to approve products')

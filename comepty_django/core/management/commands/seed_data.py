from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Tag


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@comepty.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))

        demo_user, _ = User.objects.get_or_create(username='demo', defaults={
            'email': 'demo@comepty.com',
        })
        if _:
            demo_user.set_password('demo1234')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user (demo/demo1234)'))

        categories = ['Electronics', 'Fashion', 'Home & Garden', 'Sports', 'Art & Crafts', 'Books', 'Music', 'Food']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name)
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))

        tags_list = ['trending', 'new', 'sale', 'featured', 'popular', 'limited', 'exclusive']
        for tag_name in tags_list:
            Tag.objects.get_or_create(name=tag_name)
        self.stdout.write(self.style.SUCCESS('Seed data complete!'))

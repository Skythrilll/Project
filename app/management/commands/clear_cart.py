from django.core.management.base import BaseCommand
from app.models import Cart
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Clear all cart items or cart items for a specific user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username to clear cart for (if not provided, clears all carts)',
        )

    def handle(self, *args, **options):
        username = options.get('user')
        
        if username:
            try:
                user = User.objects.get(username=username)
                cart_items = Cart.objects.filter(user=user)
                count = cart_items.count()
                
                self.stdout.write(f'\nCart items for user "{username}":')
                for item in cart_items:
                    self.stdout.write(f'  - {item.product.title} (Qty: {item.quantity})')
                
                cart_items.delete()
                self.stdout.write(self.style.SUCCESS(f'\nSuccessfully deleted {count} cart item(s) for user "{username}"'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User "{username}" not found'))
        else:
            # Show all cart items first
            all_items = Cart.objects.all()
            count = all_items.count()
            
            self.stdout.write(f'\nTotal cart items in database: {count}')
            if count > 0:
                self.stdout.write('\nCart items by user:')
                for item in all_items:
                    self.stdout.write(f'  - User: {item.user.username}, Product: {item.product.title}, Qty: {item.quantity}')
            
            # Clear all
            all_items.delete()
            self.stdout.write(self.style.SUCCESS(f'\nSuccessfully deleted all {count} cart item(s)'))

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gp.settings')
django.setup()

from django.db import connection
from app.models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist

print("=" * 50)
print("SQLite Database Connection Test")
print("=" * 50)


cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
# Displaying the database connection status and tables
print("\n✓ Database Connection: SUCCESS")
print(f"✓ Database File: {connection.settings_dict['NAME']}")
print(f"\nTotal Tables: {len(tables)}")
print("\nTables in Database:")
for table in tables:
    print(f"  - {table[0]}")

# Here we ae testing the models and  counting the records in each table
print("\n" + "=" * 50)
print("Model Data Summary")
print("=" * 50)
print(f"Products: {Product.objects.count()}")
print(f"Customers: {Customer.objects.count()}")
print(f"Cart Items: {Cart.objects.count()}")
print(f"Payments: {Payment.objects.count()}")
print(f"Orders: {OrderPlaced.objects.count()}")
print(f"Wishlist Items: {Wishlist.objects.count()}")

# Sample query to fetch and display a few products
print("\n" + "=" * 50)
print("Sample Product Query Test")
print("=" * 50)
products = Product.objects.all()[:5]
if products:
    for product in products:
        print(f"  - {product.title}: ${product.discounted_price}")
else:
    print("  No products found in database")

print("\n" + "=" * 50)
print("✓ All Database Tests Passed Successfully!")
print("=" * 50)

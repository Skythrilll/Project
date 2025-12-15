"""
SQLite Database Management Utilities for Django Grocery App
Run this script for various database operations
"""

import django
import os
import sys
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gp.settings')
django.setup()

from django.db import connection
from app.models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist
from django.contrib.auth.models import User


def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def test_connection():
    """Test database connection"""
    print_header("Database Connection Test")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT sqlite_version();")
        version = cursor.fetchone()[0]
        print(f"✓ Connected to SQLite version: {version}")
        print(f"✓ Database: {connection.settings_dict['NAME']}")
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


def list_tables():
    """List all tables in database"""
    print_header("Database Tables")
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    print(f"Total Tables: {len(tables)}\n")
    for i, table in enumerate(tables, 1):
        print(f"{i:2}. {table[0]}")


def show_statistics():
    """Show database statistics"""
    print_header("Database Statistics")
    
    stats = {
        "Users": User.objects.count(),
        "Products": Product.objects.count(),
        "Customers": Customer.objects.count(),
        "Cart Items": Cart.objects.count(),
        "Payments": Payment.objects.count(),
        "Orders": OrderPlaced.objects.count(),
        "Wishlist Items": Wishlist.objects.count(),
    }
    
    for model, count in stats.items():
        print(f"{model:<20}: {count:>5}")


def show_products():
    """Display all products"""
    print_header("Products in Database")
    products = Product.objects.all()
    
    if not products:
        print("No products found.")
        return
    
    print(f"Total Products: {products.count()}\n")
    print(f"{'ID':<5} {'Title':<30} {'Category':<10} {'Price':<10}")
    print("-" * 60)
    
    for product in products:
        category_name = dict(Product._meta.get_field('category').choices).get(product.category, product.category)
        print(f"{product.id:<5} {product.title[:28]:<30} {category_name:<10} ${product.discounted_price:<9.2f}")


def show_customers():
    """Display all customers"""
    print_header("Customers in Database")
    customers = Customer.objects.all()
    
    if not customers:
        print("No customers found.")
        return
    
    print(f"Total Customers: {customers.count()}\n")
    print(f"{'ID':<5} {'Name':<25} {'City':<15} {'State':<15}")
    print("-" * 65)
    
    for customer in customers:
        print(f"{customer.id:<5} {customer.name[:23]:<25} {customer.city[:13]:<15} {customer.state:<15}")


def show_orders():
    """Display all orders"""
    print_header("Orders in Database")
    orders = OrderPlaced.objects.all().select_related('customer', 'product')
    
    if not orders:
        print("No orders found.")
        return
    
    print(f"Total Orders: {orders.count()}\n")
    print(f"{'ID':<5} {'Customer':<20} {'Product':<25} {'Status':<15}")
    print("-" * 70)
    
    for order in orders:
        print(f"{order.id:<5} {order.customer.name[:18]:<20} {order.product.title[:23]:<25} {order.status:<15}")


def show_cart_items():
    """Display all cart items"""
    print_header("Cart Items in Database")
    cart_items = Cart.objects.all().select_related('user', 'product')
    
    if not cart_items:
        print("No cart items found.")
        return
    
    print(f"Total Cart Items: {cart_items.count()}\n")
    print(f"{'ID':<5} {'User':<20} {'Product':<30} {'Qty':<5} {'Total':<10}")
    print("-" * 75)
    
    for item in cart_items:
        print(f"{item.id:<5} {item.user.username[:18]:<20} {item.product.title[:28]:<30} {item.quantity:<5} ${item.total_cost:<9.2f}")


def show_wishlist_items():
    """Display all wishlist items"""
    print_header("Wishlist Items in Database")
    wishlist_items = Wishlist.objects.all().select_related('user', 'product')
    
    if not wishlist_items:
        print("No wishlist items found.")
        return
    
    print(f"Total Wishlist Items: {wishlist_items.count()}\n")
    print(f"{'ID':<5} {'User':<20} {'Product':<30} {'Price':<10}")
    print("-" * 70)
    
    for item in wishlist_items:
        print(f"{item.id:<5} {item.user.username[:18]:<20} {item.product.title[:28]:<30} ${item.product.discounted_price:<9.2f}")


def check_integrity():
    """Check database integrity"""
    print_header("Database Integrity Check")
    try:
        cursor = connection.cursor()
        cursor.execute("PRAGMA integrity_check;")
        result = cursor.fetchone()[0]
        if result == "ok":
            print("✓ Database integrity: OK")
        else:
            print(f"✗ Database integrity issues: {result}")
    except Exception as e:
        print(f"✗ Error checking integrity: {e}")


def database_info():
    """Show database file information"""
    print_header("Database File Information")
    db_path = connection.settings_dict['NAME']
    
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        size_kb = size / 1024
        size_mb = size_kb / 1024
        
        print(f"Location: {db_path}")
        print(f"Size: {size:,} bytes ({size_kb:.2f} KB / {size_mb:.2f} MB)")
        print(f"Modified: {datetime.fromtimestamp(os.path.getmtime(db_path))}")
    else:
        print(f"✗ Database file not found: {db_path}")


def vacuum_database():
    """Optimize database (VACUUM)"""
    print_header("Database Optimization")
    try:
        cursor = connection.cursor()
        print("Running VACUUM command...")
        cursor.execute("VACUUM;")
        print("✓ Database optimized successfully")
    except Exception as e:
        print(f"✗ Error optimizing database: {e}")


def analyze_database():
    """Analyze database for query optimization"""
    print_header("Database Analysis")
    try:
        cursor = connection.cursor()
        print("Running ANALYZE command...")
        cursor.execute("ANALYZE;")
        print("✓ Database analyzed successfully")
    except Exception as e:
        print(f"✗ Error analyzing database: {e}")


def menu():
    """Display interactive menu"""
    while True:
        print("\n" + "=" * 60)
        print(" SQLite Database Management Menu")
        print("=" * 60)
        print("1.  Test Connection")
        print("2.  List All Tables")
        print("3.  Show Statistics")
        print("4.  Show Products")
        print("5.  Show Customers")
        print("6.  Show Orders")
        print("7.  Show Cart Items")
        print("8.  Show Wishlist Items")
        print("9.  Check Database Integrity")
        print("10. Database File Info")
        print("11. Optimize Database (VACUUM)")
        print("12. Analyze Database")
        print("=" * 60)
        
        choice = input("\nEnter your choice (0-13): ").strip()
        
        if choice == '1':
            test_connection()
        elif choice == '2':
            list_tables()
        elif choice == '3':
            show_statistics()
        elif choice == '4':
            show_products()
        elif choice == '5':
            show_customers()
        elif choice == '6':
            show_orders()
        elif choice == '7':
            show_cart_items()
        elif choice == '8':
            show_wishlist_items()
        elif choice == '9':
            check_integrity()
        elif choice == '10':
            database_info()
        elif choice == '11':
            vacuum_database()
        elif choice == '12':
            analyze_database()
        elif choice == '13':
            test_connection()
            list_tables()
            show_statistics()
            check_integrity()
            database_info()
        elif choice == '0':
            print("\nGoodbye!")
            break
        else:
            print("\n✗ Invalid choice. Please try again.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        cmd = sys.argv[1].lower()
        commands = {
            'test': test_connection,
            'tables': list_tables,
            'stats': show_statistics,
            'products': show_products,
            'customers': show_customers,
            'orders': show_orders,
            'cart': show_cart_items,
            'wishlist': show_wishlist_items,
            'check': check_integrity,
            'info': database_info,
            'vacuum': vacuum_database,
            'analyze': analyze_database,
        }
        
        if cmd in commands:
            commands[cmd]()
        else:
            print(f"Unknown command: {cmd}")
            print(f"Available commands: {', '.join(commands.keys())}")
    else:
        # Interactive menu mode
        menu()

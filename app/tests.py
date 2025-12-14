from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from decimal import Decimal
import io
from PIL import Image
from .models import Product, Customer, Cart, Wishlist, Payment, OrderPlaced


# Unit testing for models and views

class ProductModelTest(TestCase):
    """Test Product model"""
    
    def setUp(self):
        # Create a mock image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        self.product = Product.objects.create(
            title="Test Ghee",
            selling_price=100.00,
            discounted_price=80.00,
            description="Premium quality ghee",
            compostion="Pure cow ghee",
            category="GH",
            product_image=SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")
        )
    
    def test_product_creation(self):
        """Test product is created correctly"""
        self.assertEqual(self.product.title, "Test Ghee")
        self.assertEqual(self.product.selling_price, 100.00)
        self.assertEqual(self.product.discounted_price, 80.00)
        self.assertEqual(self.product.category, "GH")
    
    def test_product_str(self):
        """Test product string representation"""
        self.assertEqual(str(self.product), "Test Ghee")
    
    def test_product_discount_calculation(self):
        """Test product has correct discount"""
        discount = self.product.selling_price - self.product.discounted_price
        self.assertEqual(discount, 20.00)


class CustomerModelTest(TestCase):
    """Test Customer model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.customer = Customer.objects.create(
            user=self.user,
            name="Test User",
            locality="Test Street",
            city="Dublin",
            mobile="1234567890",
            zipcode="12345",
            state="Dublin"
        )
    
    def test_customer_creation(self):
        """Test customer is created correctly"""
        self.assertEqual(self.customer.name, "Test User")
        self.assertEqual(self.customer.city, "Dublin")
        self.assertEqual(self.customer.user.username, "testuser")
    
    def test_customer_str(self):
        """Test customer string representation"""
        self.assertEqual(str(self.customer), "Test User")


class CartModelTest(TestCase):
    """Test Cart model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='cartuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            title="Test Product",
            selling_price=50.00,
            discounted_price=40.00,
            category="CR"
        )
        self.cart = Cart.objects.create(
            user=self.user,
            product=self.product,
            quantity=2
        )
    
    def test_cart_creation(self):
        """Test cart item is created correctly"""
        self.assertEqual(self.cart.quantity, 2)
        self.assertEqual(self.cart.user.username, "cartuser")
        self.assertEqual(self.cart.product.title, "Test Product")
    
    def test_cart_total_cost(self):
        """Test cart total cost calculation"""
        expected_cost = self.product.discounted_price * self.cart.quantity
        self.assertEqual(self.cart.total_cost, expected_cost)
    
    def test_cart_user_relationship(self):
        """Test cart is properly linked to user"""
        user_carts = Cart.objects.filter(user=self.user)
        self.assertEqual(user_carts.count(), 1)
        self.assertEqual(user_carts.first().product.title, "Test Product")


class WishlistModelTest(TestCase):
    """Test Wishlist model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='wishuser',
            password='testpass123'
        )
        self.product = Product.objects.create(
            title="Wishlist Product",
            selling_price=100.00,
            discounted_price=80.00,
            category="GH"
        )
        self.wishlist = Wishlist.objects.create(
            user=self.user,
            product=self.product
        )
    
    def test_wishlist_creation(self):
        """Test wishlist item is created correctly"""
        self.assertEqual(self.wishlist.user.username, "wishuser")
        self.assertEqual(self.wishlist.product.title, "Wishlist Product")
    
    def test_wishlist_user_relationship(self):
        """Test wishlist is properly linked to user"""
        user_wishlist = Wishlist.objects.filter(user=self.user)
        self.assertEqual(user_wishlist.count(), 1)
        self.assertEqual(user_wishlist.first().product.title, "Wishlist Product")


# Integration testing  

class HomeViewTest(TestCase):
    """Test home page view"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page_status_code(self):
        """Test home page loads successfully"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_page_template(self):
        """Test home page uses correct template"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'app/home.html')


class CategoryViewTest(TestCase):
    """Test category view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create a mock image for all products
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        mock_image = SimpleUploadedFile("category_test.jpg", image_io.read(), content_type="image/jpeg")
        
        # Create test products with images
        Product.objects.create(
            title="Ghee Product 1",
            selling_price=100.00,
            discounted_price=80.00,
            category="GH",
            description="Test ghee 1",
            product_image=mock_image
        )
        
        # Create new image for second product
        image_io.seek(0)
        mock_image2 = SimpleUploadedFile("category_test2.jpg", image_io.read(), content_type="image/jpeg")
        Product.objects.create(
            title="Ghee Product 2",
            selling_price=120.00,
            discounted_price=100.00,
            category="GH",
            description="Test ghee 2",
            product_image=mock_image2
        )
        
        # Create new image for third product
        image_io.seek(0)
        mock_image3 = SimpleUploadedFile("category_test3.jpg", image_io.read(), content_type="image/jpeg")
        Product.objects.create(
            title="Curd Product",
            selling_price=50.00,
            discounted_price=40.00,
            category="CR",
            description="Test curd",
            product_image=mock_image3
        )
    
    def test_category_view_status_code(self):
        """Test category page loads successfully"""
        response = self.client.get(reverse('category', args=['GH']))
        self.assertEqual(response.status_code, 200)
    
    def test_category_view_filters_correctly(self):
        """Test category view shows only products from that category"""
        response = self.client.get(reverse('category', args=['GH']))
        self.assertEqual(len(response.context['product']), 2)
    
    def test_category_excludes_cow_and_bar_products(self):
        """Test category view excludes cow and bar products"""
        # Create mock image
        image = Image.new('RGB', (100, 100), color='green')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        Product.objects.create(
            title="Cow Milk",
            selling_price=50.00,
            discounted_price=40.00,
            category="ML",
            description="Cow milk product",
            product_image=SimpleUploadedFile("cow_milk.jpg", image_io.read(), content_type="image/jpeg")
        )
        response = self.client.get(reverse('category', args=['ML']))
        products = response.context['product']
        for product in products:
            self.assertNotIn('cow', product.title.lower())
            self.assertNotIn('bar', product.title.lower())


class ProductDetailViewTest(TestCase):
    """Test product detail view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create mock image
        image = Image.new('RGB', (100, 100), color='yellow')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        self.product = Product.objects.create(
            title="Detail Product",
            selling_price=100.00,
            discounted_price=80.00,
            category="GH",
            description="Detail description",
            product_image=SimpleUploadedFile("detail_product.jpg", image_io.read(), content_type="image/jpeg")
        )
    
    def test_product_detail_status_code(self):
        """Test product detail page loads successfully"""
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_template(self):
        """Test product detail uses correct template"""
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertTemplateUsed(response, 'app/productdetail.html')
    
    def test_product_detail_context(self):
        """Test product detail has correct context"""
        response = self.client.get(reverse('product-detail', args=[self.product.id]))
        self.assertEqual(response.context['product'].title, "Detail Product")


class SearchViewTest(TestCase):
    """Test search functionality"""
    
    def setUp(self):
        self.client = Client()
        
        # Create mock images
        image = Image.new('RGB', (100, 100), color='orange')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        Product.objects.create(
            title="Premium Ghee",
            selling_price=100.00,
            discounted_price=80.00,
            description="High quality ghee",
            category="GH",
            product_image=SimpleUploadedFile("ghee_search.jpg", image_io.read(), content_type="image/jpeg")
        )
        
        image_io.seek(0)
        Product.objects.create(
            title="Fresh Curd",
            selling_price=50.00,
            discounted_price=40.00,
            description="Creamy curd",
            category="CR",
            product_image=SimpleUploadedFile("curd_search.jpg", image_io.read(), content_type="image/jpeg")
        )
    
    def test_search_view_status_code(self):
        """Test search page loads successfully"""
        response = self.client.get(reverse('search'), {'q': 'ghee'})
        self.assertEqual(response.status_code, 200)
    
    def test_search_finds_products(self):
        """Test search returns matching products"""
        response = self.client.get(reverse('search'), {'q': 'ghee'})
        products = response.context['products']
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].title, "Premium Ghee")
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        response = self.client.get(reverse('search'), {'q': ''})
        self.assertEqual(len(response.context['products']), 0)


class CartFunctionalityTest(TestCase):
    """Test cart operations (Integration Test)"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='cartuser',
            password='testpass123'
        )
        
        # Create mock image
        image = Image.new('RGB', (100, 100), color='purple')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        self.product = Product.objects.create(
            title="Cart Product",
            selling_price=100.00,
            discounted_price=80.00,
            category="GH",
            description="Cart test product",
            product_image=SimpleUploadedFile("cart_product.jpg", image_io.read(), content_type="image/jpeg")
        )
    
    def test_add_to_cart_requires_login(self):
        """Test add to cart requires authentication"""
        response = self.client.get(reverse('add-to-cart'), {'prod_id': self.product.id})
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_add_to_cart_authenticated(self):
        """Test authenticated user can add to cart"""
        self.client.login(username='cartuser', password='testpass123')
        response = self.client.get(reverse('add-to-cart'), {'prod_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        
        # Check cart item was created
        cart_count = Cart.objects.filter(user=self.user).count()
        self.assertEqual(cart_count, 1)
    
    def test_plus_cart_increases_quantity(self):
        """Test plus cart increases quantity"""
        self.client.login(username='cartuser', password='testpass123')
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        
        response = self.client.get(reverse('pluscart'), {'prod_id': self.product.id})
        cart.refresh_from_db()
        self.assertEqual(cart.quantity, 2)
    
    def test_minus_cart_decreases_quantity(self):
        """Test minus cart decreases quantity"""
        self.client.login(username='cartuser', password='testpass123')
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=2)
        
        response = self.client.get(reverse('minuscart'), {'prod_id': self.product.id})
        cart.refresh_from_db()
        self.assertEqual(cart.quantity, 1)
    
    def test_minus_cart_deletes_when_zero(self):
        """Test minus cart deletes item when quantity reaches 0"""
        self.client.login(username='cartuser', password='testpass123')
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        
        response = self.client.get(reverse('minuscart'), {'prod_id': self.product.id})
        cart_exists = Cart.objects.filter(id=cart.id).exists()
        self.assertFalse(cart_exists)
    
    def test_remove_cart_deletes_item(self):
        """Test remove cart deletes item immediately"""
        self.client.login(username='cartuser', password='testpass123')
        cart = Cart.objects.create(user=self.user, product=self.product, quantity=5)
        
        response = self.client.get(reverse('removecart'), {'prod_id': self.product.id})
        cart_exists = Cart.objects.filter(id=cart.id).exists()
        self.assertFalse(cart_exists)


class WishlistFunctionalityTest(TestCase):
    """Test wishlist operations"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='wishuser',
            password='testpass123'
        )
        
        # Create mock image
        image = Image.new('RGB', (100, 100), color='pink')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        self.product = Product.objects.create(
            title="Wishlist Product",
            selling_price=100.00,
            discounted_price=80.00,
            category="GH",
            description="Wishlist test product",
            product_image=SimpleUploadedFile("wishlist_product.jpg", image_io.read(), content_type="image/jpeg")
        )
    
    def test_add_to_wishlist(self):
        """Test adding product to wishlist"""
        self.client.login(username='wishuser', password='testpass123')
        response = self.client.get(reverse('pluswishlist'), {'prod_id': self.product.id})
        
        wishlist_count = Wishlist.objects.filter(user=self.user).count()
        self.assertEqual(wishlist_count, 1)
    
    def test_remove_from_wishlist(self):
        """Test removing product from wishlist"""
        self.client.login(username='wishuser', password='testpass123')
        Wishlist.objects.create(user=self.user, product=self.product)
        
        response = self.client.get(reverse('minuswishlist'), {'prod_id': self.product.id})
        wishlist_count = Wishlist.objects.filter(user=self.user).count()
        self.assertEqual(wishlist_count, 0)


class ContactFormTest(TestCase):
    """Test contact form submission"""
    
    def setUp(self):
        self.client = Client()
    
    def test_contact_page_get(self):
        """Test contact page loads"""
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/contact.html')
    
    def test_contact_form_submission(self):
        """Test contact form can be submitted"""
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'subject': 'Test Subject',
            'message': 'Test message content'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success


class UserAuthenticationTest(TestCase):
    """Test user authentication workflows"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='authuser',
            password='testpass123',
            email='auth@example.com'
        )
    
    def test_login_view(self):
        """Test login page loads"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_successful_login(self):
        """Test user can login successfully"""
        response = self.client.post(reverse('login'), {
            'username': 'authuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_profile_requires_login(self):
        """Test profile page requires authentication"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_accessible_when_logged_in(self):
        """Test authenticated user can access profile"""
        self.client.login(username='authuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)




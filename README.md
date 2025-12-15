# 🛒 Grocery Store - Django E-commerce Application

A full-featured online grocery store built with Django 3.2.25, specializing in premium dairy products including Ghee, Paneer, Cheese, Curd, Lassi, Milkshakes, and more.

---

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Testing](#testing)
- [Configuration](#configuration)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### User Management
- ✅ User Registration and Authentication
- ✅ User Profile Management
- ✅ Password Change Functionality
- ✅ Address Management (Multiple Addresses)

### Product Features
- ✅ Product Browsing by Category
- ✅ Product Detail Pages with Images
- ✅ Advanced Search Functionality
- ✅ Product Filtering (excludes specific items like cow milk and bars)
- ✅ Responsive Product Grid Layout

### Shopping Cart
- ✅ Add to Cart with AJAX
- ✅ Real-time Cart Updates
- ✅ Increase/Decrease Quantity
- ✅ Remove Items from Cart
- ✅ Dynamic Cart Count Badge in Navbar
- ✅ Shopping Cart Total Calculation

### Wishlist
- ✅ Add/Remove Products to Wishlist
- ✅ Wishlist Count Badge in Navbar
- ✅ Persistent Wishlist Storage

### Contact & Support
- ✅ Contact Form with Email Functionality
- ✅ Gmail SMTP Integration
- ✅ Form Validation

### UI/UX
- ✅ Bootstrap 5 Responsive Design
- ✅ Modern Navigation with Poppins Font
- ✅ Beautiful Logo with Icons
- ✅ Smooth Animations and Transitions
- ✅ Mobile-Friendly Interface
- ✅ Image Carousel on Homepage

---

## 🚀 Technology Stack

### Backend
- **Django 3.2.25** - Web Framework
- **Python 3.7.1** - Programming Language
- **Django administration** - Database (Development)
- **SQLite Database(for data storage)


### Frontend
- **Bootstrap 5.3.8** - CSS Framework
- **jQuery 3.7.1** - JavaScript Library
- **Font Awesome** - Icons
- **Google Fonts (Poppins)** - Typography
- **Owl Carousel** - Image Slider

### Email
- **Gmail SMTP** - Email Service
- **Django Email Backend** - Email Integration

---

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd grocery-app
```

### Step 2: Create Virtual Environment
```bash
python -m venv env
```

### Step 3: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\env\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
env\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### Step 4: Install Dependencies
```bash
cd gp
pip install -r requirements.txt
```

### Step 5: Configure Email Settings
Edit `gp/settings.py` and add your Gmail App Password:
```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Step 6: Run Migrations
```bash
python manage.py migrate
```

### Step 7: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 📁 Project Structure

```
grocery-app/
├── env/                          # Virtual environment
├── gp/                           # Main project directory
│   ├── app/                      # Main application
│   │   ├── migrations/           # Database migrations
│   │   ├── static/               # Static files (CSS, JS, Images)
│   │   │   └── app/
│   │   │       ├── css/          # Stylesheets
│   │   │       ├── images/       # Product images, banners
│   │   │       └── js/           # JavaScript files
│   │   ├── templates/            # HTML templates
│   │   │   └── app/
│   │   │       ├── base.html     # Base template
│   │   │       ├── home.html     # Homepage
│   │   │       ├── category.html # Category listing
│   │   │       ├── productdetail.html
│   │   │       ├── addtocart.html
│   │   │       ├── checkout.html
│   │   │       ├── contact.html
│   │   │       └── ...
│   │   ├── management/           # Custom management commands
│   │   │   └── commands/
│   │   │       └── clear_cart.py
│   │   ├── admin.py              # Admin configuration
│   │   ├── models.py             # Database models
│   │   ├── views.py              # View controllers
│   │   ├── forms.py              # Django forms
│   │   ├── urls.py               # URL routing
│   │   ├── context_processors.py # Global context
│   │   └── tests.py              # Test suite
│   ├── gp/                       # Project settings
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # Main URL configuration
│   │   └── wsgi.py               # WSGI config
│   ├── media/                    # User uploaded files
│   │   └── product/              # Product images
│   ├── db.sqlite3                # SQLite database
│   ├── manage.py                 # Django management script
│   ├── TEST_DOCUMENTATION.md     # Testing documentation
│   └── EMAIL_SETUP_GUIDE.md      # Email setup guide
└── README.md                     # This file
```

---

## 🎯 Usage

### Running the Application

1. **Activate Virtual Environment:**
   ```bash
   .\env\Scripts\Activate.ps1
   ```

2. **Navigate to Project Directory:**
   ```bash
   cd gp
   ```

3. **Start Server:**
   ```bash
   python manage.py runserver
   ```

### Admin Panel
Access at: `http://127.0.0.1:8000/admin/`

### Key URLs
- Homepage: `/`
- Product Categories: `/category/<category_code>/`
- Product Detail: `/product-detail/<product_id>/`
- Cart: `/cart/`
- Checkout: `/checkout/`
- Profile: `/profile/`
- Contact: `/contact/`
- Search: `/search/?q=<query>`

---

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run with Verbose Output
```bash
python manage.py test --verbosity=2
```

### Run Specific Test Class
```bash
python manage.py test app.tests.CartFunctionalityTest
```

### Test Coverage
- **35 Total Tests**
- **11 Unit Tests** (Models)
- **24 Integration Tests** (Views, Authentication, Workflows)
- **100% Pass Rate**

For detailed testing documentation, see: `TEST_DOCUMENTATION.md`

---

## ⚙️ Configuration

### Database Models

#### Product
- Title, Description, Composition
- Selling Price, Discounted Price
- Category (Curd, Milk, Lassi, Milkshake, Paneer, Ghee, Cheese)
- Product Image

#### Customer
- User (Foreign Key)
- Name, Locality, City, State
- Mobile, Zipcode

#### Cart
- User, Product
- Quantity
- Total Cost (Property)

#### Wishlist
- User, Product

#### Payment
- User, Amount
- Razorpay Integration Fields
- Payment Status

#### OrderPlaced
- User, Customer, Product
- Quantity, Status
- Order Date
- Payment (Foreign Key)

### Category Codes
- `CR` - Curd
- `ML` - Milk
- `LS` - Lassi
- `MS` - Milkshake
- `PN` - Paneer
- `GH` - Ghee
- `CZ` - Cheese
- `IC` - Ice Cream (commented out)

### Email Configuration
Gmail SMTP settings configured in `settings.py`:
- Host: smtp.gmail.com
- Port: 587
- TLS: Enabled

**Setup Guide:** See `EMAIL_SETUP_GUIDE.md`

---

## 🎨 Features Showcase

### Dynamic Cart Management
- Real-time updates without page refresh
- AJAX-powered add/remove operations
- Visual feedback with badges
- Automatic badge hiding when cart is empty

### Smart Product Filtering
- Excludes "cow" and "bar" products automatically
- Category-based filtering
- Search across title, description, and category

### User Experience
- Poppins font for modern typography
- Smooth hover animations
- Responsive design for all devices
- Intuitive navigation
- Beautiful product cards with images

### Context Processors
Global variables available in all templates:
- `totalitem` - Cart item count
- `wishitem` - Wishlist item count

---

## 🛠️ Custom Management Commands

### Clear Cart
```bash
# Clear all cart items
python manage.py clear_cart

# Clear cart for specific user
python manage.py clear_cart --user username
```

---

## 📧 Email Setup

To enable contact form emails:

1. Enable 2-Step Verification in Gmail
2. Generate App Password at: https://myaccount.google.com/apppasswords
3. Add to `settings.py`:
   ```python
   EMAIL_HOST_PASSWORD = 'your-16-char-app-password'
   ```
4. Restart server

---

## 🔐 Security Notes

- CSRF protection enabled on all forms
- User authentication required for cart/wishlist
- Password hashing with Django's built-in system
- SQL injection protection via Django ORM
- XSS protection in templates

---

## 📱 Responsive Design

- Mobile-first approach
- Bootstrap 5 grid system
- Responsive navigation with hamburger menu
- Optimized images for faster loading
- Touch-friendly interface

---

## 🚧 Known Issues

None currently. All 35 tests passing.

---

## 🔮 Future Enhancements

- [ ] Payment gateway integration (Razorpay/Stripe)
- [ ] Order tracking system
- [ ] Product reviews and ratings
- [ ] Email notifications for orders
- [ ] Discount coupon system
- [ ] Product inventory management
- [ ] Admin dashboard analytics
- [ ] Multi-language support
- [ ] Social media authentication

---

## 👥 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Your Name**
- Email: c18adarsh@gmail.com
- Project: Grocery Store E-commerce Platform

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Team
- Font Awesome
- Google Fonts
- Dodla Dairy (Product Inspiration)

---

## 📞 Support

For support and queries:
- Use the contact form on the website
- Email: c18adarsh@gmail.com

---

## 🎓 Learning Resources

Built as part of learning:
- Django Web Framework
- E-commerce Application Development
- AJAX and Dynamic Updates
- Payment Integration
- Email Services
- Testing in Django

---

**⭐ If you find this project useful, please consider giving it a star!**

---

*Last Updated: December 15, 2025*




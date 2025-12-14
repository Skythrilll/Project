from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from .models import Product, CATEGORY_CHOICES, Customer, Cart, Wishlist
from django.db.models import Count, Sum 
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.
def home(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/home.html", locals())

def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, "app/about.html", locals())

def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        print("=" * 80)
        print("CONTACT FORM SUBMISSION RECEIVED")
        print("=" * 80)
        print(f"From: {name}")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print("=" * 80)
        
        # Compose email
        email_subject = f'Contact Form: {subject}'
        email_message = f"""
New Contact Form Submission

From: {name}
Email: {email}
Phone: {phone}

Subject: {subject}

Message:
{message}
"""
        
        try:
            from django.core.mail import send_mail
            send_mail(
                email_subject,
                email_message,
                email,  # From email
                ['c18adarsh@gmail.com'],  # To email
                fail_silently=False,
            )
            print("✓ Email sent successfully!")
            print("=" * 80)
            messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
        except Exception as e:
            print(f"✗ Email sending failed: {str(e)}")
            print("=" * 80)
            messages.error(request, f'Sorry, there was an error sending your message: {str(e)}')
        
        return redirect('contact')
    
    return render(request, "app/contact.html", locals())

def search(request):
    query = request.GET.get('q', '')
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    products = []
    if query:
        # Search in product title, description, and category (exclude cow-milk and bars)
        products = Product.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__icontains=query)
        ).exclude(
            Q(title__icontains='cow') | 
            Q(title__icontains='bar')
        )
    
    return render(request, 'app/search.html', {
        'products': products,
        'query': query,
        'totalitem': totalitem
    })



class CategoryView(View):
    def get(self, request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val).exclude(
            Q(title__icontains='cow') | 
            Q(title__icontains='bar')
        )
        # list of products' titles in this category (if needed)
        title = product.values('title')
        # pass categories choices so the sidebar can link to other categories
        categories = CATEGORY_CHOICES
        # get human-readable current category label
        current_category = dict(CATEGORY_CHOICES).get(val, '')
        context = {
            'product': product,
            'title': title,
            'categories': categories,
            'current_category': current_category,
        }
        return render(request, 'app/category.html', context)
    
class ProductDetail(View):
    def get(self,request,pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)
        
        totalitem = 0
        wishlist = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        
        context = {
            'product': product,
            'wishlist': wishlist,
            'totalitem': totalitem,
        }
        return render(request,'app/productdetail.html', context)
    

class CustomerRegistrationView(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! Registered Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/customerregistration.html', locals())
         
class ProfileView(View):
    def dispatch(self, request, *args, **kwargs):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            form = CustomerProfileForm(instance=customer)
        except Customer.DoesNotExist:
            form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form})
    
    def post(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            customer = Customer(user=request.user)
        
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Error saving profile. Please check the form for errors.')
        
        return render(request, 'app/profile.html', {'form': form})
    
@login_required(login_url='login')
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user)) 
    return render(request, 'app/address.html', {'add': add})

class UpdateAddress(View):
    def dispatch(self, request, *args, **kwargs):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html', {'form': form})
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.zipcode = form.cleaned_data['zipcode']
            add.state = form.cleaned_data['state']
            add.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('address')
        else:
            messages.error(request, 'Error updating address. Please check the form for errors.')
            return render(request, 'app/updateAddress.html', {'form': form})
       
@login_required(login_url='login')
def add_to_cart(request):  
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    # Check if item already exists in cart
    cart_item = Cart.objects.filter(user=user, product=product).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart(user=user, product=product).save()
    
    # Return JSON response with updated cart count (number of unique products)
    cart_count = Cart.objects.filter(user=user).count()
    data = {
        'message': 'Product added to cart',
        'cart_count': cart_count
    }
    return JsonResponse(data)

@login_required(login_url='login')
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    for p in cart:
        value=p.quantity * p.product.discounted_price
        amount+=value
        totalamount = amount + 5.00
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html',locals())

class checkout(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 5.00
        return render(request, 'app/checkout.html', locals())

@login_required(login_url='login')
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 5.00
        cart_count = Cart.objects.filter(user=user).count()
        print(prod_id)
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            'cart_count': cart_count
        }
        return JsonResponse(data)
    
@login_required(login_url='login')
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        if c.quantity <= 0:
            c.delete()
        else:
            c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 5.00
        cart_count = Cart.objects.filter(user=user).count()
        data={
            'quantity': 0 if c.quantity <= 0 else c.quantity,
            'amount': amount,
            'totalamount': totalamount,
            'cart_count': cart_count
        }
        return JsonResponse(data)
    
@login_required(login_url='login')
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount += value
        totalamount = amount + 5.00
        cart_count = Cart.objects.filter(user=user).count()
        print(prod_id)
        data={
            'amount': amount,
            'totalamount': totalamount,
            'cart_count': cart_count
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        Wishlist(user=request.user, product=product).save()
        data={
            'message': 'Product added to wishlist'
        }
        return JsonResponse(data)
    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        w = Wishlist.objects.get(Q(product=product) & Q(user=request.user))
        w.delete()
        data={
            'message': 'Product removed from wishlist'
        }
        return JsonResponse(data)



        
    





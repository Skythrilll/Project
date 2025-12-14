from .models import Cart, Wishlist

def cart_wishlist_count(request):
    """Context processor to provide cart and wishlist counts to all templates"""
    totalitem = 0
    wishitem = 0
    
    if request.user.is_authenticated:
        # Count number of unique products in cart
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()
    
    return {
        'totalitem': totalitem,
        'wishitem': wishitem,
    }

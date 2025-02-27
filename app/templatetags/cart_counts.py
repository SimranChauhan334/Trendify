
from django import template
from app.models import AddToCart

register = template.Library()

@register.simple_tag
def count_cart(request):

    if not request.user.is_authenticated:
        return 0

    cart_items = AddToCart.objects.filter(user=request.user)
    
    
    total_quantity = sum(cart_item.quantity for cart_item in cart_items)

    return total_quantity

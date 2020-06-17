from zoup_app.constants import ACCOUNT_TYPES
from zoup_app.models.vendor import Cart


def cart_item_count_processor(request):
    cart_item_count = 0
    if request.user.is_authenticated and request.user.account_type == ACCOUNT_TYPES['CUSTOMER']:
        try:
            cart_item_count = request.user.cart.item_count
        except Cart.DoesNotExist:
            cart = Cart(user=request.user)
            cart.save()
            cart_item_count = cart.item_count

    return {'cart_item_count': cart_item_count}

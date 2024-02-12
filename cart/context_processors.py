from .cart import Cart
from .favorite import Favorite


def cart(request):
    return {'cart': Cart(request)}


def favorites(request):
    return {'favorites': Favorite(request)}

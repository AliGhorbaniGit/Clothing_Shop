from .cart import Cart


def cart(request):
    #Cart.update(request)

    return {'cart': Cart(request)}

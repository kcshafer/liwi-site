import logging

from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader, RequestContext

from cart.models import Cart, CartLineItem

log = logging.getLogger('liwi')

def view_cart(request):
    user_id = request.session.get('user_id', None)
    session_key = request.session.session_key
    cart = None
    cart_items = []
    cart_aggr = None

    if Cart.objects.filter(user_id=user_id).exists():
        cart = Cart.objects.get(user_id=user_id)
    elif Cart.objects.filter(session_key=session_key).exists():
        cart = Cart.objects.get(session_key=session_key)
    else:
        if user_id:
            cart = Cart.objects.create(user_id=user_id)
        else:
            cart = Cart.objects.create(session_key=session_key)

    cart_items = CartLineItem.objects.all().filter(cart_id=cart.id).select_related('art__title')
    if user_id:
        cart_aggr = Cart.objects.filter().aggregate(Sum('cartlineitem__art__price'))
    else:
        cart_aggr = Cart.objects.filter(session_key=session_key).aggregate(Sum('cartlineitem__art__price'))

    context = RequestContext(request, {'cart': cart, 'cart_items': cart_items, 'cart_aggr': cart_aggr})
    template = loader.get_template('cart/view_cart.html')

    return HttpResponse(template.render(context))

def add_to_cart(request, art_id):
    user_id = request.session.get('user_id', None)
    session_key = request.session.session_key
    cart = None
    cart_items = []

    if Cart.objects.filter(user_id=user_id).exists():
        cart = Cart.objects.get(user_id=user_id)
    elif Cart.objects.filter(session_key=session_key).exists():
        cart = Cart.objects.get(session_key=session_key)
    else:
        if user_id:
            cart = Cart.objects.create(user_id=user_id)
        else:
            cart = cart.objects.create(session_key=session_key)

    cli = CartLineItem.objects.create(cart_id=cart.id, art_id=art_id)

    return HttpResponse("added")

def remove_from_cart(request, cli_id):
    CartLineItem.objects.get(id=cli_id).delete()

    return HttpResponse("Deleted")

def empty_cart(request):
    user_id = request.session.get('user_id', None)
    session_key = request.session.session_key
    cart = None

    if Cart.objects.filter(user_id=user_id).exists():
        cart = Cart.objects.get(user_id=user_id)
    elif Cart.objects.filter(session_key=session_key).exists():
        cart = Cart.objects.get(session_key=session_key)

    CartLineItem.objects.all().filter(cart_id=cart.id).delete();

    return HttpResponse('Emptied');
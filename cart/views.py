import logging

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader, RequestContext

from cart.models import Cart, CartLineItem

log = logging.getLogger('liwi')

def view_cart(request):
    user_id = request.session.get('user_id', None)
    session_key = request.session.session_key
    cart = None
    cart_items = []

    if Cart.objects.filter(user_id=user_id).exists():
        cart = Cart.objects.get(user_id=user_id)
    elif Cart.objects.filter(session_key=session_key).exists():
        cart = Cart.objects.get(session_key=session_key)
    else:
        cart = Cart.objects.create(session_key=session_key, user_id=user_id)

    cart_items = CartLineItem.objects.all().filter(cart_id=cart.id).select_related('art__title')

    context = RequestContext(request, {'cart': cart, 'cart_items': cart_items})
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
        cart = Cart.objects.create(session_key=session_key, user_id=user_id)

    cli = CartLineItem.objects.create(cart_id=cart.id, art_id=art_id)

    return HttpResponse("added")
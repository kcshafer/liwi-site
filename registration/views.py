from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext

from registration.forms import CustomerRegistration, SellerRegistration


def index(request):
    template = loader.get_template('registration/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def artlover_form(request):
    if request.method == 'POST':
        user_form = CustomerRegistration(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.type = 'customer'
            user.is_artist = False
            user.set_password(user.password)
            user.save()

        return HttpResponse('Post request submitted for artlover')
    else:
        user_form = CustomerRegistration()
        return render(
            request,
                'registration/register.html',
                {'user_form': user_form}
            )

def seller_form(request):
    if request.method == 'POST':
        user_form = SellerRegistration(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.is_artist = True
            user.type = 'seller'
            user.set_password(user.password)
            user.save()

        return HttpResponse('Account created successfully')
    else:
        user_form = CustomerRegistration()
        template = loader.get_template('registration/buyer_form.html')
        context = RequestContext(request, {'user_form': user_form})
        return HttpResponse(template.render(context))


from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, RequestContext

from registration.forms import CustomerRegistration, SellerRegistration
from registration.models import User

def index(request):
    template = loader.get_template('registration/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def artlover_form(request):
    if request.method == 'POST':
        user_form = CustomerRegistration(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.type = 'customer'
            user.is_artist = False
            user.set_password(user.password)
            user.save()
        return HttpResponse('Account created successfully')
    else:
        #TODO: use template.render for form
        user_form = CustomerRegistration(initial={'is_artist':False})
        return render(
            request,
                'registration/buyer_form.html',
                {'user_form': user_form}
            )

def seller_form(request):
    if request.method == 'POST':
        user_form = SellerRegistration(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_artist = True
            user.is_active = False
            user.type = 'seller'
            user.set_password(user.password)
            user.save()
            email_message = "Your Liwi account was created, activate it by clicking the link. localhost:8000/registration/activate/%s" % (user.id)
            msg = EmailMultiAlternatives('Activate User', email_message , 'noreply@liwi.co', [user.email])
            html_email = "<a href='localhost:8000/registration/activate/%s'>Activate</a>" % (user.id)
            msg.attach_alternative(html_email, "text/html")
            resp = msg.send()
        return HttpResponse('Account created successfully')
    else:
        user_form = SellerRegistration(initial={'is_artist':True})
        template = loader.get_template('registration/register.html')
        context = RequestContext(request, {'user_form': user_form})
        return HttpResponse(template.render(context))

def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
    else:
        messages.add_message(request, messages.ERROR, 'Invalid request. User is already activated.')

    return HttpResponseRedirect('/auth/')


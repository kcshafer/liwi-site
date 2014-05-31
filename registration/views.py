from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext

from registration.forms import CustomerRegistration


def index(request):
    template = loader.get_template('registration/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def artlover_form(request):
    if request.method == 'POST':
        user_form = CustomerRegistration(data=request.POST)
        print user_form.errors
        if user_form.is_valid():
            print "in save"
            user = user_form.save()

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

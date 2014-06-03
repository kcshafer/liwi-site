from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, RequestContext

from registration.models import User
from user_profile.models import Profile

def view_profile(request, user_id):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    template = loader.get_template('user_profile/view_profile.html')
    context = RequestContext(request, {'user': user})

    return HttpResponse(template.render(context))

@login_required
def edit_profile(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    return HttpResponse('Viewing profile for %s' % (user.email))
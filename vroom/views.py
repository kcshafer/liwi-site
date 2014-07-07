import logging
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader, RequestContext

from art.models import Art
from registration.models import User


def index(request, art_id):
    art = Art.objects.get(id=art_id)
        
    context = RequestContext(request, {'art': art})
    template = loader.get_template('vr/virtual_room.html')
    return HttpResponse(template.render(context))

def upload(request):
    session_key = request.session.session_key
    data = request.FILES['file']
    f = open('photos/temp/%s' % (data._name), 'w+')
    f.write(data.read())
    f.close()

    return HttpResponse('test')

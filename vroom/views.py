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
    session_key = request.session.session_key
    files = []
    if os.path.isdir('photos/temp/%s' % session_key):
        print "here"
        files = os.listdir('photos/temp/%s' % session_key)
    else:
        os.mkdir('temp/%s' % session_key)
    
    context = RequestContext(request, {'files': files, 'session_key': session_key, 'art': art})
    template = loader.get_template('vr/virtual_room.html')
    return HttpResponse(template.render(context))

def upload(request):
    session_key = request.session.session_key
    data = request.FILES['file'] 
    f = open('photos/temp/%s/test.jpg' % session_key, 'w+')
    f.write(data.read())
    f.close()

    return HttpResponse('test')

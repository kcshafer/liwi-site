from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template import loader, RequestContext

from registration.models import User

def index(request):
    artists = User.objects.all().filter(is_artist=True)[:10]
    template = loader.get_template('artists/artists_view.html')
    context = RequestContext(request, {'artists': artists})

    return HttpResponse(template.render(context))
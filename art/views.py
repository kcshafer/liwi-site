from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template import loader, RequestContext

from art.forms import ArtForm
from art.models import Art
from registration.models import User

#index is multi view
def index(request):
    art = Art.objects.all()[:10]
    template = loader.get_template('art/art_multi_view.html')
    context = RequestContext(request, {'art' : art})

    return HttpResponse(template.render(context))

@login_required
def create_art_form(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    if user.is_artist:
        art_form = ArtForm()
        template = loader.get_template('art/art_form.html')
        context = RequestContext(request, {'art_form': art_form})
        return HttpResponse(template.render(context))
    else:
        return HttpResponse('Only registered artists can post artwork for sale.')

def upload(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        art_form = ArtForm(request.POST, request.FILES)
        if art_form.is_valid():
            art = art_form.save(commit=False)
            art.user_id = user_id
            art.save()
            return HttpResponse('Art created')
        else:
            print art_form.errors
            return HttpResponse(art_form.errors)
    else:
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')

def view_art_single(request, art_id):
    art = Art.objects.get(id=art_id)
    template = loader.get_template('art/art_view.html')
    context = RequestContext(request, {'art': art})

    return HttpResponse(template.render(context))
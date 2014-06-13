import ast

from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template import loader, RequestContext

from art.forms import ArtForm
from art.models import Art, Like, ArtTag
from registration.models import User

#index is multi view
def index(request):
    template = loader.get_template('art/art_multi_view.html')
    if request.user.is_authenticated():
        user_id = request.session['user_id']
        #TODO: optimize this
        liked_art = Like.objects.all().filter(user_id=user_id)
        liked_art_ids = []
        for la in liked_art:
            liked_art_ids.append(la.art_id)
        art = Art.objects.all()
        context = RequestContext(request, {'art' : art, 'liked_art': liked_art_ids})
    else:
        art = Art.objects.all()
        context = RequestContext(request, {'art' : art})

    return HttpResponse(template.render(context))

@login_required
def create_art_form(request, category=None, sub_category=None):
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
            category = ast.literal_eval(art_form['categories'].value())
            print art_form.cleaned_data
            art.category = category.get('name')
            art.user_id = user_id
            art.save()
            for tag in art_form['tags'].value():
                tag = ast.literal_eval(tag)
                ArtTag.objects.create(art_id=art.id, tag_id=tag[1])
            return HttpResponseRedirect('/art/view/%s' % (art.id))
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

@login_required
def like_art(request, art_id):
    user_id = request.session['user_id']
    art_user_like = "%s_%s" % (user_id, art_id)
    Like.objects.create(user_id=user_id, art_id=art_id, art_user_like=art_user_like)

    return HttpResponse('Liked!')

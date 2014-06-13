from django.shortcuts import render
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template import loader, RequestContext

from art.forms import ArtForm
from art.lib.categorytree import CategoryTree
from art.models import Art, Like
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
def select_art_category(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    if user.is_artist:
        template = loader.get_template('art/category_form.html')
        category_tree = CategoryTree()
        categories = category_tree.categories
        context = RequestContext(request, {'categories': categories})
        cache.set('cat_tree': category_tree)
        return HttpResponse(template.render(context))
    else:
        return HttpResponse('Only registered artists can post artwork for sale.')

@login_required
def create_art_form(request, category=None, sub_category=None):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    if user.is_artist:
        art_form = ArtForm()
        template = loader.get_template('art/art_form.html')
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


###### METHODS CALLED FROM AJAX #######
@login_request:
def get_subcategories(request, cat_id):
    category_tree = cache.get('cat_tree')
    sub_cats = category_tree.get_subs(cat_id)

    return sub_cats

@login_required
def like_art(request, art_id):
    user_id = request.session['user_id']
    art_user_like = "%s_%s" % (user_id, art_id)
    Like.objects.create(user_id=user_id, art_id=art_id, art_user_like=art_user_like)

    return HttpResponse('Liked!')


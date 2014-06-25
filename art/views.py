import ast
import logging

from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader, RequestContext

from art.forms import ArtForm
from art.models import Art, Like, ArtTag, Tag
from registration.models import User

log = logging.getLogger('liwi')

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
        art = Art.objects.all().filter(active=True)
        tags = cache.get('tags')
        if not tags:
            tags = Tag.objects.all().values('name')
            tags = [t.get('name') for t in tags]
        context = RequestContext(request, {'art' : art, 'liked_art': liked_art_ids, 'tags': tags})
    else:
        art = Art.objects.all()
        context = RequestContext(request, {'art' : art})

    return HttpResponse(template.render(context))

@login_required
def my_art_admin(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    if user.is_artist:
        art = Art.objects.values('title', 'id', 'photo', 'active').annotate(likes=Count('like'))
        tags = cache.get('tags')
        if not tags:
            tags = Tag.objects.all().values('name')
            tags = [t.get('name') for t in tags]
        context = RequestContext(request, {'art': art, 'tags': tags})
        template = loader.get_template('art/my_art_view.html')
        return HttpResponse(template.render(context))
    else:
        messages.add_message(request, messages.WARNING, 'Only artists can view the my art admin page')
        return HttpResponseRedirect('/')


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
        log.warn("Non artist attempted to post art with user id %s" % user_id)
        return HttpResponse('Only registered artists can post artwork for sale.')

def upload(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        art_form = ArtForm(request.POST, request.FILES)
        if art_form.is_valid():
            art = art_form.save(commit=False)
            category = ast.literal_eval(art_form['categories'].value())
            art.category = category.get('name')
            art.user_id = user_id
            art.save()
            for tag in art_form['tags'].value():
                tag = ast.literal_eval(tag)
                ArtTag.objects.create(art_id=art.id, tag_id=tag[1])
            return HttpResponseRedirect('/art/view/%s' % (art.id))
        else:
            return HttpResponse(art_form.errors)
    else:
        log.warn("Unauthorized post request made to upload view")
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

@login_required
def unlike_art(request, art_id):
    if request.method == 'POST':
        user_id = request.session['user_id']
        Like.objects.get(user_id=user_id, art_id=art_id).delete()
        return HttpResponse('Unliked!')
    else:
        log.warn("Unauthorized post request made to art activate view")
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')

@login_required
def handle_art_activation(request, art_id):
    if request.method == 'POST':
        art = Art.objects.get(id=art_id)
        art.active = False if art.active is True else True
        art.save()
        return HttpResponse('Deactivate' if art.active is True else 'Activate')
    else:
        log.warn("Unauthorized post request made to art activate view")
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')
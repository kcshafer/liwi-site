from datetime import datetime
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.template import loader, RequestContext

from artists.forms import FeaturedArtistForm
from artists.models import FeaturedArtist
from registration.models import User

log = logging.getLogger('liwi')


def index(request):
    artists = User.objects.raw('select registration_user.id, registration_user.username, user_profile.photo from registration_user inner join user_profile on registration_user.id=user_profile.user_id where is_active=True and is_artist=True')
    template = loader.get_template('artists/artists_view.html')
    context = RequestContext(request, {'artists': artists})

    return HttpResponse(template.render(context))


@login_required
def get_featured(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if user.is_artist:
        existing_fa = FeaturedArtist.objects.all().filter(user_id=user_id, active=True)
        if existing_fa:
            messages.add_message(request, messages.WARNING, 'You have an active feature currently, come back after %s to renew!' % existing_fa[0].end_date)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            template = loader.get_template('artists/get_featured_form.html')
            fa_form = FeaturedArtistForm()
            context = RequestContext(request, {'fa_form': fa_form})
            return HttpResponse(template.render(context))
    else:
        messages.add_message(request, messages.WARNING, 'Only artists are allowed to be featured')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def get_featured_register(request):
    if request.method == 'POST':
        print request.POST
        user_id = request.session.get('user_id')
        fa_form = FeaturedArtistForm(request.POST)
        print fa_form.__dict__
        if fa_form.is_valid():
            featured_artist = fa_form.save(commit=False)
            featured_artist.user_id = user_id
            featured_artist.active = True
            featured_artist.last_imprint = datetime.now()
            featured_artist.total_imprints = 0
            featured_artist.save()
            messages.add_message(request, messages.SUCCESS, 'Registered as a featured artist!')
            return HttpResponseRedirect('/')
        else:
            template = loader.get_template('artists/get_featured_form.html')
            context = RequestContext(request, {'fa_form': fa_form})
            return HttpResponse(template.render(context))
    else:
        log.error("Unauthorized get request made to get featured")
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')
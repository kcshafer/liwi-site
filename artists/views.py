from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader, RequestContext

from registration.models import User

def index(request):
    artists = User.objects.raw('select registration_user.id, registration_user.username, user_profile.photo from registration_user inner join user_profile on registration_user.id=user_profile.user_id where is_active=True and is_artist=True')
    template = loader.get_template('artists/artists_view.html')
    context = RequestContext(request, {'artists': artists})

    return HttpResponse(template.render(context))
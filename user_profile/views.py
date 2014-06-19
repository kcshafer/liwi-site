from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render
from django.template import loader, RequestContext

from art.models import Art, Like
from registration.models import User
from user_profile.forms import MyProfileForm
from user_profile.models import Profile

def view_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user_id=user_id)
    art = Art.objects.all().filter(user_id=user_id)
    liked_art = Like.objects.filter(user_id=user.id).values('art__title', 'art__photo')
    template = loader.get_template('user_profile/view_profile.html')
    context = RequestContext(request, {'usr': user, 'profile': profile, 'art': art, 'liked_art': liked_art})

    return HttpResponse(template.render(context))

@login_required
def edit_profile(request):
    uid = request.session['user_id']
    profile = Profile.objects.get(user_id=uid)
    profile_form = MyProfileForm(instance=profile)
    template = loader.get_template('user_profile/edit_profile.html')
    context = RequestContext(request, {'profile_form': profile_form})
    return HttpResponse(template.render(context))

@login_required
def save_profile(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        profile = Profile.objects.get(user_id=user_id)
        profile_form = MyProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile = profile_form.save()
            profile.save()
        return HttpResponseRedirect('/profile/view/%s' % (user_id))
    else:
        #this might need to return something more ui friendly
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')
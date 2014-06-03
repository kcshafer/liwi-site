from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template import loader, RequestContext

from authentication.forms import LoginForm

def index(request):
    print request.session
    login_form = LoginForm()
    return render(
        request,
        'authentication/login_form.html',
        {'login_form': login_form}
    )
    return HttpResponse('This is the auth index')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponse('User not found or password incorrect')
    else:
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/auth')
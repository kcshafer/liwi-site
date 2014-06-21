from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.template import loader, RequestContext

from authentication.forms import LoginForm
from registration.models import User, SecurityAnswer, SecurityQuestion

#Note: the index is where the login form is rendered
def index(request):
    login_form = LoginForm()
    next = request.GET.get('next')
    template = loader.get_template('authentication/login_form.html')
    context = RequestContext(request, {'login_form': login_form, 'next': next})

    return HttpResponse(template.render(context))

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user_id'] = user.id
            if request.POST.get('next', None) is not None:
                return HttpResponseRedirect(request.POST.get('next'))
            else:
                return HttpResponseRedirect('/')
        else:
            return HttpResponse('User not found or password incorrect')
    else:
        #this might need to return something more ui friendly
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).count():
            user = User.objects.get(username=username)
            cache.set('user_id', user.id, 30)
            return HttpResponseRedirect('/resetpassword/valid/')
        else:
            messages.add_message(request, messages.ERROR, 'Username does not exist, please try again.')
            return HttpResponseRedirect('forgotpassword/') 
    else:
        template = loader.get_template('authentication/forgot_password.html')
        context = RequestContext(request)
        return HttpResponse(template.render(context))

def validate_answer(request):
    if request.method == 'POST':
        user_id = cache.get('user_id')
        if user_id:
            answer = request.POST.get('secret_answer')
            secret_answer = SecurityAnswer.objects.get(user_id=user_id)
            if secret_answer.answer == answer:
                return HttpResponseRedirect('resetpassword/')
            else:
                messages.add_message(request, messages.ERROR, 'Incorrect answer')
                return HttpResponseRedirect('valid')
        else:
            messages.add_message(request, messages.ERROR, 'Request timed out, please try again.')
            return HttpResponseRedirect('forgotpassword/')
    else:
        user_id = cache.get('user_id')
        if user_id:
            secret_answer = SecurityAnswer.objects.get(user_id=user_id)
            secret_question = SecurityQuestion.objects.get(id=secret_answer.security_questions_id)
            context = RequestContext(request, {'secret_question': secret_question})
            template = loader.get_template('authentication/security_questions.html')
            cache.set('user_id', user_id, 30)
            return HttpResponse(template.render(context))
        else:
            messages.add_message(request, messages.ERROR, 'Request timed out, please try again.')
            return HttpResponseRedirect('forgotpassword/')

def reset_password(request):
    if request.method == 'POST':
        user_id = cache.get('user_id')
        if user_id:
            password = request.POST.get('password')
            re_password = request.POST.get('re_password')
            if password == re_password:
                secure_pw = make_password(password)
                password = None
                re_password = None
                user = User.objects.get(id=user_id)
                user.password = secure_pw
                user.save()
                return HttpResponseRedirect('/login/')
            else:
                messages.add_message(request, messages.ERROR, 'Passwords did not match try again')
                cache.set('user_id', user_id, 30)
                return HttpResponse('/resetpassword/')
        else:
            messages.add_message(request, messages.ERROR, 'Request timed out, please try again.')
            return HttpResponseRedirect('/forgotpassword/')
    else:
        user_id = cache.get('user_id')
        context = RequestContext(request)
        template = loader.get_template('authentication/reset_password.html')
        cache.set('user_id', user_id, 30)
        return HttpResponse(template.render(context))

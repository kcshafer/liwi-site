import ast
import logging
from os import mkdir 

from django.contrib.auth import hashers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader, RequestContext
from django.shortcuts import render_to_response

from registration.forms import CustomerRegistration, SellerRegistration, AccountForm
from registration.models import User, SecurityAnswer
from user_profile.models import Profile
from liwi import globals

#TODO: This has to go
if globals.PRODUCTION:
    from settings import production as settings
else:
    from settings import development as settings

log = logging.getLogger('liwi')


def index(request):
    template = loader.get_template('registration/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def artlover_form(request):
    if request.method == 'POST':
        user_form = CustomerRegistration(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.type = 'customer'
            user.is_artist = False
            user.is_active = False
            user.set_password(user.password)
            user.save()
            #TODO: find a way to properly handle this
            #catching when there isn't a secret answer 
            try:
                secret_question = ast.literal_eval(user_form['secret_question'].value())
                secret_answer_val = user_form['secret_answer'].value()
                secret_answer = SecurityAnswer()
                secret_answer.user_id = user.id
                secret_answer.security_questions_id = secret_question.get('id')
                secret_answer.answer = secret_answer_val
                secret_answer.save()
            except Exception as e:
                pass
            email_message = "Your Liwi account was created, activate it by clicking the link. localhost:8000/registration/activate/%s" % (user.id)
            msg = EmailMultiAlternatives('Activate User', email_message , 'liwimail2014@gmail.com', [user.email])
            html_email = "<a href='http://ec2-54-213-188-46.us-west-2.compute.amazonaws.com/registration/activate/%s'>Activate</a>" % (user.id)
            msg.attach_alternative(html_email, "text/html")
            resp = msg.send()
            messages.add_message(request, messages.SUCCESS, 'Account created, an email was sent to your email with instructions to activate your account.')
            return HttpResponseRedirect('/login/')
        else:
            template = loader.get_template('registration/buyer_form.html')
            context = RequestContext(request, {'user_form': user_form})
            return HttpResponse(template.render(context))

    else:
        user_form = CustomerRegistration(initial={'is_artist':False})
        template = loader.get_template('registration/buyer_form.html')
        context = RequestContext(request, {'user_form': user_form})
        return HttpResponse(template.render(context))        

def seller_form(request):
    if request.method == 'POST':
        user_form = SellerRegistration(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_artist = True
            user.is_active = False
            user.type = 'seller'
            user.set_password(user.password)
            user.save()
            #TODO: find a way to properly handle this
            #catching when there isn't a secret answer 
            try:
                secret_question = ast.literal_eval(user_form['secret_question'].value())
                secret_answer_val = user_form['secret_answer'].value()
                secret_answer = SecurityAnswer()
                secret_answer.user_id = user.id
                secret_answer.security_questions_id = secret_question.get('id')
                secret_answer.answer = secret_answer_val
                secret_answer.save()
            except Exception as e:
                print e.args
                #TODO: ponder what to do with this
                pass
            email_message = "Your Liwi account was created, activate it by clicking the link. localhost:8000/registration/activate/%s" % (user.id)
            msg = EmailMultiAlternatives('Activate User', email_message , 'liwimail2014@gmail.com', [user.email])
            html_email = "<a href='http://ec2-54-213-188-46.us-west-2.compute.amazonaws.com/registration/activate/%s'>Activate</a>" % (user.id)
            msg.attach_alternative(html_email, "text/html")
            resp = msg.send()
            messages.add_message(request, messages.SUCCESS, 'Account created, an email was sent to your email with instructions to activate your account.')
            return HttpResponseRedirect('/login/')
        else:
            template = loader.get_template('registration/register.html')
            context = RequestContext(request, {'user_form': user_form})
            return HttpResponse(template.render(context))
    else:
        user_form = SellerRegistration(initial={'is_artist':True})
        template = loader.get_template('registration/register.html')
        context = RequestContext(request, {'user_form': user_form})
        return HttpResponse(template.render(context))

def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    if not user.is_active:
        user.is_active = True
        Profile.objects.create(user_id=user_id)
        mkdir('%suser/%s' % (settings.MEDIA_ROOT,user_id))
        user.save()
    else:
        log.warn("User with id %s trying to activate when already active" % user.id)
        messages.add_message(request, messages.ERROR, 'Invalid request. User is already activated.')

    return HttpResponseRedirect('/login/')

@login_required
def view_account(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    template = loader.get_template('account/view_account.html')
    context = RequestContext(request, {'usr': user})
    return HttpResponse(template.render(context))

@login_required
def edit_account(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    acct_form = AccountForm(instance=user)
    template = loader.get_template('account/edit_account.html')
    context = RequestContext(request, {'acct_form': acct_form})
    return HttpResponse(template.render(context))

@login_required()
def save_account(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        acct_form = AccountForm(request.POST, instance=user)
        if acct_form.is_valid():
            user = acct_form.save()
            user.save()
        return HttpResponseRedirect('/account/')
    else:
        #this might need to return something more ui friendly
        log.warn("Unauthorized post request made to save account")
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')

@login_required
def change_password(request):
    if request.method == 'POST':
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        re_new_password = request.POST.get('re_new_password')
        if hashers.check_password(old_password, user.password):
            if new_password == re_new_password:
                secure_password = hashers.make_password(new_password)
                user.password = secure_password
                user.save()
                messages.add_message(request, messages.SUCCESS, 'Password changed successfully')
                return HttpResponseRedirect('/account/')
            else:
                messages.add_message(request, messages.SUCCESS, 'Passwords do not match.')
                return HttpResponseRedirect('/account/edit/')
        else:
                messages.add_message(request, messages.SUCCESS, 'Incorrect password')
                return HttpResponseRedirect('/account/edit/')
    else:
        log.warn("Unauthorized post request made to change password")
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')


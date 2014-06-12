import ast
from os import mkdir 

from django.core.mail  import get_connection
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, RequestContext

from registration.forms import CustomerRegistration, SellerRegistration
from registration.models import User, SecurityAnswer
from user_profile.models import Profile
from liwi import settings

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
            except:
                #TODO: ponder what to do with this
                pass
            email_message = "Your Liwi account was created, activate it by clicking the link. localhost:8000/registration/activate/%s" % (user.id)
            msg = EmailMultiAlternatives('Activate User', email_message , 'liwimail2014@gmail.com', [user.email])
            html_email = "<a href='localhost:8000/registration/activate/%s'>Activate</a>" % (user.id)
            msg.attach_alternative(html_email, "text/html")
            resp = msg.send()
        messages.add_message(request, messages.SUCCESS, 'Account created, an email was sent to your email with instructions to activate your account.')
        return HttpResponseRedirect('/login/')
    else:
        user_form = SellerRegistration(initial={'is_artist':False})
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
            except:
                #TODO: ponder what to do with this
                pass
            email_message = "Your Liwi account was created, activate it by clicking the link. localhost:8000/registration/activate/%s" % (user.id)
            msg = EmailMultiAlternatives('Activate User', email_message , 'liwimail2014@gmail.com', [user.email])
            html_email = "<a href='localhost:8000/registration/activate/%s'>Activate</a>" % (user.id)
            msg.attach_alternative(html_email, "text/html")
            resp = msg.send()
        messages.add_message(request, messages.SUCCESS, 'Account created, an email was sent to your email with instructions to activate your account.')
        return HttpResponseRedirect('/login/')
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
        messages.add_message(request, messages.ERROR, 'Invalid request. User is already activated.')

    return HttpResponseRedirect('/login/')


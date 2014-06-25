import logging

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template import loader, RequestContext

from artists.lib.featured_artist import retrieve_featured_artists

log = logging.getLogger('liwi')

def index(request):
    template = loader.get_template('home/index.html')
    featured_artists = retrieve_featured_artists(5)
    context = RequestContext(request, {'featured_artists': featured_artists})
    return HttpResponse(template.render(context))

def contact(request):
    template = loader.get_template('home/contact.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def contact_send(request):
    if request.method == 'POST':
        email_message = request.POST.get('body')
        subject = request.POST.get('subject')
        from_email = request.POST.get('email')
        if from_email and subject and email_message:
            msg = EmailMultiAlternatives(subject, email_message , from_email, ['kcplusplus@live.com'])
            resp = msg.send()
            messages.add_message(request, messages.SUCCESS, 'Message sent successfully, we will be in contact with you as soon as possible')
            return HttpResponseRedirect('/contact/')
        else:
            if not from_email:
                messages.add_message(request, messages.ERROR, 'Email not provided')
            if not subject:
                messages.add_message(request, messages.ERROR, 'Subject cannot be blank')
            if not email_message:
                messages.add_message(request, messages.ERROR, 'Message cannot be blank')

            return HttpResponseRedirect('/contact/')

    else:
        log.warn("Unauthorized post request made to save account")
        return HttpResponseNotAllowed(['POST'], 'Unauthorized Request.')

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import contactForm
# from django.core.mail import send_mail
# from django.conf import settings


def contact(request):
    if request.method == 'POST':
        form = contactForm(request.POST)

        if form.is_valid():
            pass
            '''
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            subject = 'Message from MYSITE.com'
            message = '%s %s' % (comment, name)
            emailFrom = form.cleaned_data['email']
            emailTo = [settings.EMAIL_HOST_USER]

            send_mail(
                subject,
                message,
                emailFrom,
                emailTo,
                fail_silently=True
            )
            '''

    else:
        form = contactForm()
    args = {
        'form': form
    }
    return render(request, 'contact/contact.html', args)

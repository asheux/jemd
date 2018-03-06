from __future__ import unicode_literals

from django.shortcuts import render


def site(request):
    return render(request, 'website/site.html')

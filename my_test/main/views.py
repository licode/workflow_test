from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone


def main(request):
    return render_to_response('all_beamlines.html')


def tool(request):
    return render_to_response('all_beamlines.html')

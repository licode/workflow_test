from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
import main

class FrameView(View):
    def get(self, request, *args, **kwargs):
        name = kwargs['name']
        template_name = '';
        if name == 'welcome':
            template_name = 'welcome.html'
        elif name == "tool_menu":
            template_name = 'tool_menu.html'
        return render(request, template_name, self.get_context_data())
    def get_context_data(self):
        context = {'menu': main.toolbox.toolbox.content}
        return context
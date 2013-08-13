from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
import datetime
import json
import main
from main.models import Job, OutputData

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

#from history.history_render import HistoryRender    
class HistoryView(TemplateView):
    """
    display history panel
    """
    template_name = "history.html"
    def get_context_data(self, **kwargs):
        #HR = HistoryRender()
        #'history': HR.return_content
        return {'time': str(datetime.datetime.now())}
    
class MainView(TemplateView):
    """
    website main page
    """
    template_name = "main.html"
    
class AnalyzeView(TemplateView):
    """
    main page for analyzing data function - single tool execution
    """
    template_name = "menu_base.html"
    def get_context_data(self, **kwargs):
        return {'src': '/frame/welcome/', 'selected': 'menu_tool'}

class RunView(TemplateView):
    """
    Right now it just shows a job created message
    """
    template_name = "run_notice.html"
    
def get_status(request):
   jobs = Job.objects.exclude(status=main.job.JOB_STATUS.SUCCESS)
   print jobs
   if not jobs:
       status = {'done': 1}
   else:
       status = {'done': 0}
       update_dict = {}
       import os
       path = os.getcwd()
       for job in jobs:
           filename = OutputData.objects.get(job=job).filename
	   print filename
           filename = path + '/WorkflowPrototype1/Results/' + filename
           import os.path
           if os.path.isfile(filename):
               job.status = main.job.JOB_STATUS.SUCCESS
               job.save()
               update_dict['job' + str(job.id)] = 'Succeeded'
       status['list'] = update_dict
   #status = {'done': 1, 'list':{'job1':'test'}};
   status = json.dumps(status)
   return HttpResponse(status, content_type='application/json')


class WorkflowView(TemplateView):
    """
    Right now it just shows a job created message
    """
    template_name = "workflow.html"
    
class VisualizationView(TemplateView):
    """
    Right now it just shows a job created message
    """
    template_name = "visualization.html"
    
class HelpView(TemplateView):
    """
    Right now it just shows a job created message
    """
    template_name = "help.html"    

from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
import main
import main.job
import os
from main.models import User, History, Job, ToolData

class JobView(View):
    """
    """
    template_name = 'job_detail.html'

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        job = Job.objects.get(id = id)
        tool_id = job.tool
        tool_name = main.toolbox.get_tool(tool_id).title
        info = []
        info.append("Created: %s %s" % (str(job.created_date), job.created_time.strftime("%X")))
        info.append("<br>")
        info.append("Output Size: ")
        context = self.get_context_data()
        context['input_info'] = self.get_inputs(job)
        context['basic_info'] = "\n".join(info)
        context['tool_name'] = tool_name
        return render(request, self.template_name, context)
    def get_context_data(self):
        context = {}
        return context
    def get_inputs(self, job):
        inputs = ToolData.objects.filter(job = job)
        content = []
        for item in inputs:
            content.append("%s: %s<br>" % (item.data_key, item.data_val))
        return '\n'.join(content)
            
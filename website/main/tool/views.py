from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
import main
#from main.save_data import SaveToDatabase
#from main.history_render import HistoryRender
#from job_manager.job_wrapper import JobWrapper
from main.Runner.job_runner import JobRunner


FIELD_TYPES = {
    "float": forms.FloatField,
    "int": forms.IntegerField,
    "file": forms.FileField,
    "char": forms.CharField
}


def generate_form(tool):
    fields = {}
    for item in tool.input:
        _type = item["type"]
        _label = item["label"]
        fields[_label] = FIELD_TYPES[_type](label = _label)
    return type('MyForm', (forms.Form,), fields)


class ToolView(View):
    template_name = 'tool_run.html'

    def get(self, request, *args, **kwargs):
        tool = main.toolbox.get_tool(kwargs['id'])
        form_class = generate_form(tool)
        context = self.get_context_data()
        context['form'] = form_class()
        context['tool_name'] = tool.title
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        tool = main.toolbox.get_tool(kwargs['id'])
        form_class = generate_form(tool)
        form = form_class(request.POST)
        if form.is_valid():

            myform = form.cleaned_data
            JR = JobRunner(kwargs['id'],myform)
            JR.submit_job()
            ###save to database###
            #SD = SaveToDatabase(kwargs['id'])
            #SD.save_all(myform)
            ######

            ###run jobs###
            #JW = JobWrapper()
            #JW.run_job()
            #########

            return HttpResponseRedirect(request.get_full_path() + "run/")
        
        context = self.get_context_data()
        context['form'] = form
        context['tool_name'] = tool.title
        return render(request, self.template_name, context)

    def get_context_data(self):
        context = {}
        return context


class Tool:
    def __init__(self, config):
        self.id = None
        self.input = None
        self.output = None
        self.command = None
        self.load(config)
    def load(self, config):
        if "id" in config:
            self.id = config["id"]

        if "input" in config:
            self.input = config["input"]
            #self.parse_input(config["input"])

        if "output" in config:
            self.output = config["output"]
            #self.parse_output(config["output"])

        if "command" in config:
            self.command = config["command"]

        if "title" in config:
            self.title = config["title"]


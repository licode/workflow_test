from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
import main
import os
from main.Runner.job_runner import JobRunner


FIELD_TYPES = {
    "float": forms.FloatField,
    "int": forms.IntegerField,
    "file": forms.FileField,
    "select": forms.ChoiceField,
    "char": forms.CharField
}

ROOT_DIR = os.getcwd() #this indicates that the system should be run at root directory
DATA_SOURCE_DIR = ROOT_DIR + "/results/"
def get_data_source(extension):
    """
    This function generate a list of choices used in the tool's select field as data source
    """
    import glob
    files = glob.glob(DATA_SOURCE_DIR + "*." + extension)
    source = [(f, os.path.basename(f)) for f in files]
    return source

def generate_form(tool):
    """
    This function generate a class that inherits forms.Form. This class represents
    the form used by the incoming 'tool'.
    """
    fields = {}
    for item in tool.input:
        _type = item["type"]
        _label = item["label"]
        if _type == "select":
            #process options if provided
            _choices = get_data_source("hdf5")
            fields[_label] = FIELD_TYPES[_type](label = _label, choices = _choices)
        else:
            fields[_label] = FIELD_TYPES[_type](label = _label)
    return type('MyForm', (forms.Form,), fields)

def handle_uploaded_file(f):
    with open(DATA_SOURCE_DIR + str(f), 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


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
        
        form = form_class(request.POST,request.FILES)
        if form.is_valid():
            myform = form.cleaned_data
            if kwargs['id'] == "upload":
                #need redesign in the future
                #uploaded file names could be already used
                #file should be renamed and original file name is stored as a label
                #besides, this job also need to be recorded in database
                handle_uploaded_file(request.FILES['File'])
            JR = JobRunner()
            JR.submit_job(tool, myform)
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
        self.title = None
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


from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.http import HttpResponseRedirect
#from main import toolbox
from django import forms
import main
#from main.models import ToolData, JobData
from main.save_data import SaveToDatabase

FIELD_TYPES = {
    "float": forms.FloatField,
    "int": forms.IntegerField
}

def generate_form(id):
    tool = main.toolbox.get_tool(id)
    fields = {}
    for item in tool.input:
        _type = item["type"]
        _label = item["label"]
        fields[_label] = FIELD_TYPES[_type](label = _label)
    return type('MyForm', (forms.Form,), fields)



class ToolView(View):
    template_name = 'tool_run.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        form_class = generate_form(kwargs['id'])
        context = self.get_context_data()
        context['form'] = form_class()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.form_class = generate_form(kwargs['id'])
        form = self.form_class(request.POST)
        if form.is_valid():
            myform = form.cleaned_data

            ###save to database###
            SD = SaveToDatabase(kwargs['id'])
            SD.save_all(myform)
            ######

            ###run jobs###
            #########

            return HttpResponseRedirect('/tool_run/' + kwargs['id'] + "/")

        print form.errors
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    #def get_success_url(self):
    #    return '/tool_run/' + self.tool_id
    def get_context_data(self):
        context = {'menu': main.toolbox.toolbox.content}
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


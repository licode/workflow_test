from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import main.tool.views as tv
import main.toolbox as tb
from main.models import ToolData

class MainView(TemplateView):
    template_name = "main.html"
    def get_context_data(self, **kwargs):
        return {'menu': tb.toolbox.content}

class RunView(TemplateView):
    template_name = "run_notice.html"

    def get_context_data(self, **kwargs):
        arg = ToolData.objects.get(id=1)
        output = "<li>"+str(arg.this_id)+"</li>"
        return {'menu': tb.toolbox.content,
               'val' : output}

# This includes all url dispatching except default admin/account
urlpatterns = patterns('',
    url(r'^$', MainView.as_view()),
    url(r'tool/(?P<id>\w+)/$', tv.ToolView.as_view()),
    url(r'tool_run/(?P<id>\w+)/$', RunView.as_view())
)

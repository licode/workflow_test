from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
import main.tool.views as tv
import main.toolbox as tb
from main.models import ToolData, JobData
from history_render import HistoryRender


class MainView(TemplateView):
    template_name = "main.html"
    def get_context_data(self, **kwargs):
        HR = HistoryRender()
        return {'menu': tb.toolbox.content,
                'arg': HR.return_content}

class RunView(TemplateView):
    template_name = "run_notice.html"

    def get_context_data(self, **kwargs):

        HR = HistoryRender()

        return {'menu': tb.toolbox.content,
                'arg' : HR.return_content}

# This includes all url dispatching except default admin/account
urlpatterns = patterns('',
    url(r'^$', MainView.as_view()),
    url(r'tool/(?P<id>\w+)/$', tv.ToolView.as_view()),
    url(r'tool_run/(?P<id>\w+)/$', RunView.as_view())
)

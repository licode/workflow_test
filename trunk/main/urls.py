from django.conf.urls import patterns, include, url
import main.tool.views as tv
import main.history.views as hv
import main.views
import main.job.views as jv

# This includes all url dispatching except default admin/account
urlpatterns = patterns('',
    url(r'^$', main.views.MainView.as_view()), 
    url(r'frame/(?P<name>\w+)/$', main.views.FrameView.as_view()), 
    url(r'tool/$', main.views.AnalyzeView.as_view()),
    url(r'tool/(?P<id>\w+)/$', tv.ToolView.as_view()),
    url(r'tool/(?P<id>\w+)/run/$', main.views.RunView.as_view()),
    url(r'history/$', hv.HistoryView.as_view()),
    url(r'status/$', main.views.get_status),
    url(r'job/(?P<id>\d+)/$', jv.JobView.as_view()),
    url(r'job/(?P<id>\d+)/(?P<action>\w+)/$', hv.HistoryView.as_view())
)
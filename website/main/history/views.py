from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
import main
import main.job
import os
from main.models import User, History, Job, ToolData
from main.job.user_controller import UserController

JOB_BLOCK_TEMPLATE = \
"""         <div class="jobitem" id="job{id}">
                <div class="jobnumber">{number}.</div>
                <a href="/job/{id}/delete/">
                <img class="delete_icon" src="/static/images/delete.png"/>
                </a>
                <img class="summarytrigger" src="/static/images/arrow_down.png"/>
                <div class="jobtitle"><a href="/job/{id}/" target="frame_main">{title}</a></div>
                <div id="jobstatus">{status}</div>
                <div class="summary" style="display: none">
                    {summary}
                </div>
            </div>"""
        

class HistoryView(View):
    """
    This displays the history panel
    1. get job list from current history
    2. generate html
    """
    template_name = 'history.html'

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            if kwargs['action'] == u'delete':
                self.delete_job(kwargs['id'])
        user = request.user
        print user

        history = self.get_current_history(user)
        if history is None:
            return render(request, self.template_name)
        #user = self.get_current_user()
        content = self.generate_content(history)
        context = self.get_context_data()
        context['historytitle'] = history.name
        context['content'] = content
        return render(request, self.template_name, context)
    
    def delete_job(self, id):
        job = Job.objects.filter(id = id).delete()
        
    def generate_content(self, history):
        jobs = Job.objects.filter(history = history).order_by('-id')
        #jobs = Job.objects.filter(user = user).order_by('-id')
        count = len(jobs)
        print "len: ", count
        content = []
        for index, job in enumerate(jobs):
            job_num = str(count - index)
            job_title = main.toolbox.get_tool(job.tool).title
            job_id = str(job.id)
            job_status = str(main.job.JOB_STATUS(job.status))
            job_summary = "created: %s %s" % \
                (str(job.created_date), job.created_time.strftime("%X"))
            content.append(JOB_BLOCK_TEMPLATE.format(id = job_id, 
                                                     number = job_num, 
                                                     title = job_title, 
                                                     status = job_status, 
                                                     summary = job_summary))
        return "\n".join(content)

    
    def get_context_data(self):
        context = {}
        return context
    
    def get_current_history(self,user):
        #these two functions are copied from job module, need wrap these into new class
        #user = self.get_current_user()
        try:
            histories = History.objects.filter(user=user).filter(is_current=True)
        except:
            return None
        if len(histories) == 0:
            return History.objects.create(name="Demo", user=user, size=0, is_current=True)
        assert(len(histories) == 1)
        print "return history"
        return histories[0]
        
    def get_current_user(self):
        #if User.objects.count() == 0:
        #    return User.objects.create(first_name="Mike", last_name="Li")
        #else:
        #    users = User.objects.filter(last_name="Li")
        #if len(users) != 0:
        #    return users[0]
        UC = UserController()
        user = UC.get_user()
        #print "user: ", user.first_name, user.last_name
        return user
        


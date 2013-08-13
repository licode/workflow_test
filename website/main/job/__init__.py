from main.models import User, History, Job, ToolData
import datetime
import main
from main.job.user_controller import UserController


class JOB_STATUS:
    values = {0: 'Created', 
              1: 'Ready',
              2: 'Queued',
              3: 'Running',
              4: "Succeeded",
              5: "Failed"}
    def __init__(self, value):
        self.value = value
    CREATED, READY, QUEUED, RUNNING, SUCCESS, FAIL = range(6)
    def __str__(self):
        return JOB_STATUS.values[self.value]
        
        


class JobWrapper:
    def __init__(self):
        self.job = None;
        
    def create(self, user, 
               tool, form):
        self.history = self.get_current_history(user)
        self.tool = tool
        self.status = JOB_STATUS.READY
        self.user = self.get_current_user()
        self.job = Job.objects.create(history = self.history, 
                                      tool = tool.id, 
                                      status = self.status)
        print self.job
        
        self.params = form
        for item in tool.input:
            key = item["label"]
            val = form[key]
            ToolData.objects.create(job=self.job,
                                    data_key=key,
                                    data_val=val)

    def set_status(self, status):
        assert(self.job)
        self.job.status = status
        self.job.save()
        
    def get_current_history(self, user):
        #this is a placeholder, need to call real history manager
        #user = self.get_current_user()
        histories = History.objects.filter(user=user).filter(is_current=True)
        if len(histories) == 0:
            return History.objects.create(name="Demo", user=user, size=0, is_current=True)
        assert(len(histories) == 1)
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
        return user
        
        
    def display(self, request):
        pass
    
    def delete(self, request):
        pass
    

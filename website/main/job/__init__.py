import datetime
from main.models import Job
class JOB_STATUS:
    CREATED, READY, QUEUED, RUNNING, SUCCESS, FAIL = range(6)


class JobWrapper:
    def __init(self):
        self.id = None;
    def create(self, tool, form):
        self.history = self.get_current_history()
        self.tool = tool.id
        self.status = JOB_STATUS.READY
        Job.objects.create(history = self.history, tool = self.tool, status = self.status)
        #more to come
    def get_current_history(self):
        #this is a placeholder, need to call real history manager
        return 1
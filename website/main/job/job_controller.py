from main.models import User, History, Job, ToolData
import main

class JobController(object):
    """
    save data into database:
    """

    def __init__(self, data_id):
        self.tool = main.toolbox.get_tool(data_id)
        self.data_num = 0    ###current index of tooldata
        self.fname = "Mike"
        self.lname = "Li"
        self.history_name = "history"
        self.current = True
        self.size_val = 1
        self.status = 1
        return

    def set_user(self):
        new_user = User.objects.create(first_name=self.fname,
                                       last_name=self.lname)
        return new_user

    def set_history(self):
        new_user = self.set_user()
        size_val = self.size_val   ###what is this used for?
        current = self.current
        new_history = History.objects.create(name=self.history_name,
                                             user=new_user,
                                             size=size_val, 
                                             is_current=current)
        return new_history

    def set_job(self):
        new_history = self.set_history()
        tool_name = self.tool.id
        status = self.status
        new_job = Job.objects.create(history=new_history,
                                     tool=tool_name,
                                     status=status)
        return new_job
    
    def set_tooldata(self, formdata):
        new_job = self.set_job()
        for item in self.tool.input:
            key = item["label"]
            val = formdata[key]
            ToolData.objects.create(job=new_job,
                                    data_key=key,
                                    data_val=val)
            
        return
    
    
    
    
    
    
    
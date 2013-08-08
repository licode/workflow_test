from main.models import User, History, Job, ToolData
import main

class JobController(object):
    """
    read data from forms and save them into database:
    """

    def __init__(self, data_id):
        self.tool = main.toolbox.get_tool(data_id)
        self.data_num = 0    ###current index of tooldata
        return

    def set_user(self):
        fname = "Mike"
        lname = "Li"
        new_user = User.objects.create(first_name=fname,last_name=lname)
        return new_user

    def set_history(self):
        history_name = "history"
        new_user = self.set_user()
        size_val = 1
        current = True
        new_history = History.objects.create(name=history_name,user=new_user,
                size = size_val, is_current=current)
        return new_history

    def set_job(self):
        new_history = self.set_history()
        tool_name = self.tool.id
        status = 1
        new_job = Job.objects.create(history=new_history,tool=tool_name,status=status)
        return new_job


    """
    def save_tooldata(self, formdata):
        dm = ToolData.objects.all()
        self.data_num = len(dm)+1

        for item in self.tool.input:
            key = item["label"]
            val = formdata[key]

            ToolData.objects.create(this_id=self.data_num,
                    tool_name=str(self.tool.id),
                    data_key=str(key),
                    data_val=str(val))

        return


    def save_jobdata(self):
        jd = JobData.objects.all()
        job_num = len(jd)+1

        JobData.objects.create(job_id=job_num,
                tool_id=self.data_num,
                job_status="done")

        return

    def save_all(self, formdata):
        self.save_tooldata(formdata)
        self.save_jobdata()
        return

"""





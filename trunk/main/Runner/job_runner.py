from main.models import ToolData, Job, History
from WorkflowPrototype1.workflow.workflow_user import Workflow_user
from WorkflowPrototype1.workflow.workflow_setting import brokers
import main.job
import json



class JobRunner(object):

    def __init__(self):
        #self.jobID = jobID
        self.username = "user1"
        #self.message_list = []
        self.tool_list = ["tomography","dpc"]
        self.file_path = "../static/images/"
        self.output_file = ""
        #self.tool_id = tool_id
        #self.form_data = form_data
        #self.save_job()
        return


    def create_job(self, tool, form):
        """
        access to database to save data
        """
        job = main.job.JobWrapper()
        job.create(tool, form)
        return job


    def read_jobdata(self, job):
        """
        generate message from a job object
        The message is used for activeMQ
        """

        tool_name = job.tool.id

        #dic_val = {}
        #for item in data_obj:
        #    key_v = item.data_key
        #    val_v = item.data_val
        #    dic_val[str(key_v)]=val_v

        if tool_name=="tomography":

            algorithm = job.params['algorithm']
            angle_start = job.params['angle_start']               
            angle_end = job.params['angle_end']
            angle_step = job.params['angle_step']

            username = self.username
            passcode = "pw"
            information = ""

            output_file = str(username)+"_"+tool_name+".jpeg"
            self.output_file = output_file

            message = {"instrument": "HXN",         ###save as dictionary for activeMQ
                "job": algorithm,
                "user": username,
                "passcode": passcode,
                "input_data_file": "filename.png",
                "output_data_file": self.file_path+output_file,
                "information": information,
                "method": ""}
        return message


    def submit_job(self, tool, form):
        """
        call ActiveMQ
        """
        job = self.create_job(tool, form)
        if job.tool.id == "upload":
            job.set_status(main.job.JOB_STATUS.SUCCESS)
            return
        message = self.read_jobdata(job)
        return
        username = message['user']
        passcode = message['passcode']
        wu = Workflow_user(brokers, username, passcode)
        msg = json.dumps(message)
        wu.submit(msg)

def test():
    pass


if __name__=="__main__":
    test()



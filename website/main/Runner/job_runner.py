from main.models import ToolData, Job, History, OutputData
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


    def create_job(self, user, tool, form):
        """
        access to database to save data
        """
        job = main.job.JobWrapper()
        job.create(user, tool, form)
        return job


    def read_jobdata(self, job):
        """
        generate message from a job object
        The message is used for activeMQ
        """
        #tool_name = job.tool.id
        if 'algorithm' in job.params:
            algorithm = job.params['algorithm']
        if 'File' in job.params:
            information = job.params['File']
        else:
	    information = ""
        output = job.tool.output[0]
        mode = job.tool.mode
        output_file = output['name'] + str(job.job.id) + "." + output['type']
        OutputData.objects.create(job = job.job, filename = output_file)
        return {"instrument": "HXN",         ###save as dictionary for activeMQ
               "job": algorithm,
               "user": 'user1',
               "passcode": 'pw',
               "input_data_file": "",
               "output_data_file": output_file,
               "information": information,
               "method": "",
               "mode": mode}


    def submit_job(self, user, tool, form):
        """
        call ActiveMQ
        """
        job = self.create_job(user, tool, form)
        if job.tool.id == "upload":
            job.set_status(main.job.JOB_STATUS.SUCCESS)
            return
        message = self.read_jobdata(job)
        print message
        username = message['user']
        passcode = message['passcode']
        wu = Workflow_user(brokers, username, passcode)
        msg = json.dumps(message)
        wu.submit(msg)

def test():
    pass


if __name__=="__main__":
    test()



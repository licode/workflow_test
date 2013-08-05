from main.models import ToolData, Job, History
from WorkflowPrototype1.workflow.workflow_user import Workflow_user
from WorkflowPrototype1.workflow.workflow_setting import brokers
from main.job.job_controller import JobController
import json



class JobRunner(object):

    def __init__(self, data_id, form_data):
        #self.jobID = jobID
        self.username = "user1"
        #self.message_list = []
        self.tool_list = ["tomography","dpc"]
        self.file_path = "../static/images/"
        self.output_file = ""
        self.data_id = data_id
        self.form_data = form_data
        self.save_job()
        return


    def save_job(self):
        """
        access to database to save data
        """
        JobC = JobController(self.data_id)
        JobC.set_tooldata(self.form_data)
        return


    def read_jobdata(self):
        """
        read data from database
        pass jobID to obtain parameters
        """
        #obj = JobData.objects.all()
        #jobID = len(obj)   ###return the latest job, there should be better way
        #cur_obj = JobData.objects.get(id=jobID)

        #tool_id = cur_obj.tool_id
        #tools = ToolData.objects.filter(this_id=tool_id)

        history_name = "history"
        history_obj = History.objects.filter(name=history_name)
        job_obj = Job.objects.filter(history=history_obj)
        data_obj = ToolData.objects.filter(job=job_obj)

        tool_id = job_obj[0].tool
        tool_name = tool_id

        dic_val = {}

        for item in data_obj:
            key_v = item.data_key
            val_v = item.data_val
            dic_val[str(key_v)]=val_v

        if tool_name=="tomography":

            algorithm = str(dic_val['algorithm'])
            angle_start = float(str(dic_val['angle_start']))                
            angle_end = float(str(dic_val['angle_end']))
            angle_step = float(str(dic_val['angle_step']))

            username = self.username
            passcode = "pw"

            output_file = str(username)+"_"+str(tool_id)+".jpeg"
            self.output_file = output_file
            information = str(int(angle_start))+" "+str(int(angle_end))+" "+str(int(angle_step))
            print information

            message = {"instrument": "HXN",         ###save as dictionary for activeMQ
                "job": algorithm,
                "user": username,
                "passcode": passcode,
                "input_data_file": "filename.png",
                "output_data_file": self.file_path+output_file,
                "information": information,
                "method": ""}

            #job_infor = {"jobname": toolname,
            #        "job_id":jobID}
            #self.job_list.append(job_infor)


        return message


    def submit_job(self):
        """
        call ActiveMQ
        """
        message = self.read_jobdata()
        username = message['user']
        passcode = message['passcode']
        wu = Workflow_user(brokers, username, passcode)
        msg = json.dumps(message)
        wu.submit(msg)

        return





def test():
    pass


if __name__=="__main__":
    test()



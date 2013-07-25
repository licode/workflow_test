from article.models import Article, JobData
from WorkflowPrototype1.workflow.workflow_user import Workflow_user
from WorkflowPrototype1.workflow.workflow_setting import brokers
import json



class JobWrapper(object):

    def __init__(self):
        self.job_list = []
        self.message_list = []
        return


    def readDB(self, toolname, jobID):
        """
        read data from django database
        pass jobID to obtain parameters
        """
        if toolname=="Article":
            cur_obj = Article.objects.get(id=jobID)

            job = str(cur_obj.algorithm)
            username = "user1"
            passcode = "pw"
            title = str(cur_obj.title)
            file_p = "../static/images/"

            output_file = str(username)+"_"+str(title)+".jpeg"
            information = str(int(cur_obj.angle_start))+" "+str(int(cur_obj.angle_end))+" "+str(int(cur_obj.angle_step))

            message = {"instrument": "HXN",         ###save as dictionary for activeMQ
                "job": job,
                "user": username,
                "passcode": passcode,
                "input_data_file": "filename.png",
                "output_data_file": file_p+output_file,
                "information": information,
                "method": ""}

            self.message_list.append(message)

            job_infor = {"jobname": toolname,
                    "job_id":jobID}
            self.job_list.append(job_infor)

        else:
            pass

        return


    def run_job(self, message):
        """
        call ActiveMQ
        """
        username = message['user']
        passcode = message['passcode']
        wu = Workflow_user(brokers, username, passcode)
        msg = json.dumps(message)
        wu.submit(msg)

        return


    def run_joblist(self):
        """
        run multiple jobs through activeMQ
        """

        for message in self.message_list:
            self.run_job(message)


    def saveDB(self):
        """
        save joblist to new database
        """
        job_obj = JobData.objects.all()
        new_id = len(job_obj)+1
        print new_id

        newjob = JobData()

        for job in self.job_list:
            newjob.job_id = new_id
            newjob.tool_name = job['jobname']
            newjob.tool_id = job['job_id']
            newjob.save()

        return





def test():
    pass


if __name__=="__main__":
    test()



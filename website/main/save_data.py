from main.models import ToolData, JobData
import main

class SaveToDatabase(object):
    """
    read data from forms and save them into database:
        ToolData and JobData
    """

    def __init__(self, data_id):
        self.tool = main.toolbox.get_tool(data_id)
        self.data_num = 0    ###current index of tooldata
        return

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







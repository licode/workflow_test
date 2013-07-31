from main.models import ToolData, JobData

class HistoryRender():
    """
    render history by reading data from database and organize
    """

    def __init__(self):
        self.content=[]
        return

    def get_data(self):
        job_all = JobData.objects.all()
        job_len = len(job_all)

        if job_len==0:
            return

        for m in range(job_len):
            i = job_len-m-1
            item = "<h3>Job ID: "+str(job_all[i].job_id)+" </h3>"
            self.content.append(item)
            tool_id = job_all[i].tool_id
            tool = ToolData.objects.filter(this_id=tool_id)
            item = "<li>Job name: "+str(tool[0].tool_name)+"</li>"
            self.content.append(item)
            item = "<li> Job status: done </li>"  ###edit this later
            self.content.append(item)
            for j in range(len(tool)):
                item = "<li>: "+str(tool[j].data_key)+": "+str(tool[j].data_val)+"</li>"
                self.content.append(item)
            self.content.append("<hr>")
        return


    def return_content(self):
        self.get_data()
        if len(self.content)==0:
            return self.content
        else:
            self.content = "\n".join(self.content)
            return self.content



from main.models import History, Job, ToolData

class HistoryRender():

    def __init__(self):
        self.content=[]
        #self.history_name = history_name
        return

    def get_data(self):
        his_all = History.objects.all()
        his_len = len(his_all)

        if his_len==0:
            return

        for m in range(his_len):
            i = his_len-m-1
            item = "<h3>Name: "+str(his_all[i].name)+" </h3>"
            self.content.append(item)
            
            job_obj = Job.objects.filter(history=his_all[i])
            for j in range(len(job_obj)):
                tool_name = job_obj[j].tool
                time_val = job_obj[j].created_time
                #tool_id = his_all[i].tool_id
                #tool = ToolData.objects.filter(this_id=tool_id)
                item = "<h3>Job name: "+str(tool_name)+"</h3>"
                self.content.append(item)
                item = "<h3> Job status: done </h3>"  ###edit this later
                self.content.append(item)
                tool_obj = ToolData.objects.filter(job=job_obj[j])
                for k in range(len(tool_obj)):
                    item = "<li>: "+str(tool_obj[k].data_key)+": "+str(tool_obj[k].data_val)+"</li>"
                    self.content.append(item)
                item = "<h4>Created time: "+str(time_val)+"</h4>"
            self.content.append("<hr>")
        return


    def return_content(self):
        self.get_data()
        if len(self.content)==0:
            return self.content
        else:
            self.content = "\n".join(self.content)
            return self.content


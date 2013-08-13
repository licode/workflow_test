from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponseRedirect
import main
import main.job
import os
from main.models import User, History, Job, ToolData, OutputData

import h5py
import numpy as np
from scipy.misc import imsave

if __name__ == '__main__':
    nlist = getFile('tomo_out.h5')
    print nlist


class JobView(View):
    """
    """
    template_name = 'job_detail.html'

    def get(self, request, *args, **kwargs):
        
        id = kwargs['id']
        job = Job.objects.get(id = id)
        tool_id = job.tool
        tool_name = main.toolbox.get_tool(tool_id).title
        info = []
        info.append("Created: %s %s" % (str(job.created_date), job.created_time.strftime("%X")))
        info.append("<br>")
        info.append("Output Size: ")
        context = self.get_context_data()
        context['input_info'] = self.get_inputs(job)
        context['basic_info'] = "\n".join(info)
        context['output_info'] = self.get_outputs(job, main.toolbox.get_tool(tool_id)) 
        context['tool_name'] = tool_name
        return render(request, self.template_name, context)
    def get_context_data(self):
        context = {}
        return context
    def get_inputs(self, job):
        inputs = ToolData.objects.filter(job = job)
        content = []
        for item in inputs:
            content.append("%s: %s<br>" % (item.data_key, item.data_val))
        return '\n'.join(content)

    def get_outputs(self, job, tool):
        output = OutputData.objects.get(job = job)
	import os
	path = os.getcwd()
        imagefolder = "/static/images/"
        ofile = path + '/WorkflowPrototype1/Results/' + output.filename 
	out = tool.output[0]
	if out['type'] == 'h5':
		path += imagefolder
		image_list = self.getFile(path, ofile)
	else:
		import shutil
		shutil.copy(ofile, path + imagefolder + output.filename)
                image_list = [output.filename]
        content = []
        for image in image_list:
            image = imagefolder + image
            content.append('<img width="500" src="%s"/>' % image)
            content.append('<br>')
        return '\n'.join(content)

    def getFile(self, path, h5name):
        file = h5py.File(h5name)
        data = file['/volume']
        
        namelist = []
        for i in [0, 10, 19]:
        	filename = 'tomo_' + str(i) + '.png'
        	namelist.append(filename)
        	imsave(path + filename, data[:,:,i])
        file.close()
        
        return namelist

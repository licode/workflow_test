from django.db import models

# Create your models here.


class ToolData(models.Model):
    """
    generate a much generic way to store data
    """
    this_id = models.IntegerField()               ###set as same value for different tool attributes
    tool_name = models.CharField(max_length=200)
    data_key = models.CharField(max_length=200)
    data_val = models.CharField(max_length=500)

    def __unicode__(self):
        return self.tool_name


class JobData(models.Model):
    job_id = models.IntegerField()               ###different jobdata might have the same job_id, for workflow design
    tool_id = models.IntegerField()
    job_status = models.CharField(max_length=200)   ###job status

    def __unicode__(self):
        return str(self.job_id)


class Job(models.Model):
    #history = models.ForeignKey(History)
    tool = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add = True)
    created_time = models.TimeField(auto_now_add = True)
    status = models.IntegerField()   ###job status

    def __unicode__(self):
        return str(self.tool)



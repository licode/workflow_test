from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    pass

class History(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    size = models.IntegerField()
    is_current = models.BooleanField()

class Workflow(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    #more fields to add

class Job(models.Model):
    history = models.ForeignKey(History)
    tool = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add = True)
    created_time = models.TimeField(auto_now_add = True)
    status = models.IntegerField()   ###job status

    def __unicode__(self):
        return str(self.tool)

class ToolData(models.Model):
    """
    generate a much generic way to store data
    """
    job = models.ForeignKey(Job)
    data_key = models.CharField(max_length=200)
    data_val = models.CharField(max_length=500)

    def __unicode__(self):
        return str(self.job)


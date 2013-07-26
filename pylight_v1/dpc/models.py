from django.db import models
from time import time
from django.utils import timezone


def get_upload_file_name(instance, filename):
    #return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)
    return "uploaded_files/%s" % (filename)

"""
class JobData(models.Model):
    job_id = models.IntegerField()
    tool_name = models.CharField(max_length=200)
    tool_id = models.IntegerField()

    def __unicode__(self):
        return self.title
"""

class DPCData(models.Model):
    title = models.CharField(max_length=200)
    notes = models.CharField(max_length=500)
    parameter1 = models.FloatField(default=0.0)
    parameter2 = models.FloatField(default=0.0)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=200)
    body = models.TextField()

    article = models.ForeignKey(DPCData)



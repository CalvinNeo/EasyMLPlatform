#coding:utf8

from django.db import models
from www.utils import random_file_name
from www import settings

def get_upload_to(instance, filename):
    # paths = { 'I':'images/', 'V':'videos/', 'A':'audio/', 'D':'documents'/ }
    # return settings.MEDIA_ROOT + 'content/' + paths[instance.content_type] + filename
    return settings.MEDIA_ROOT + 'upload/dataset/' + random_file_name(filename)

class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    path = models.FileField(upload_to = get_upload_to)
    filetype = models.CharField(max_length=10)  
    head = models.CharField(max_length=1023)

    class Meta:
        db_table = 'dataset'

    def __unicode__(self):
        return "#{}: ({}) {} @ {}".format(self.id,self.filetype,self.name,self.path)

def SaveDataset():
    pass
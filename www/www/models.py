# encoding: utf-8
import sys,os
sys.path.append('../')

from django.db import models
from www.utils import random_file_name
from www import settings
import datasets.localdata

def get_upload_to(instance, filename):
    # paths = { 'I':'images/', 'V':'videos/', 'A':'audio/', 'D':'documents'/ }
    # return settings.MEDIA_ROOT + 'content/' + paths[instance.content_type] + filename
    return settings.MEDIA_ROOT + 'dataset/' + random_file_name(filename)

class Dataset(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    path = models.FileField(upload_to = get_upload_to)
    filetype = models.CharField(max_length=10)  
    head = models.CharField(max_length=1023)
    attr_delim = models.CharField(max_length=3)
    record_delim = models.CharField(max_length=3)

    class Meta:
        db_table = 'dataset'

    def __unicode__(self):
        return "#{}: ({}) {} @ {} attr_delim: {} record_delim: {}".format(self.id,self.filetype,self.name,self.path,self.attr_delim,self.record_delim)

    @staticmethod
    def GetDatasets(pageindex=0, max_item=10):
        l = len(Dataset.objects.all())
        if l > 0:
            return Dataset.objects.all()[min(pageindex*max_item,l-1):min((pageindex+1)*max_item,l)]
        else:
            return {}
    @staticmethod
    def ViewDataset(unicodedatasetindex=None, maximum_items=100):
        if unicodedatasetindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            datasetindex = int(unicodedatasetindex)
            if datasetindex >= 0:
                datasetfile = Dataset.objects.get(id = datasetindex)
                #open local dataset
                lcdt = datasets.localdata.LocalData(datamapper = lambda data,colindex,head:int(data))
                lcdt.ReadString(open(str(datasetfile.path),"r").read(),hasHead=True, getValue=True)

                return lcdt
        return None

class MLModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    modeltype = models.CharField(max_length=10) 
    path = models.FileField(upload_to = lambda instance, filename:settings.MEDIA_ROOT + 'upload/models/' + random_file_name(filename))

    class Meta:
        db_table = 'models'

    def __unicode__(self):
        return "#{}: ({}) {} @ {}".format(self.id,self.modeltype,self.name,self.path)
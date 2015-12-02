# encoding: utf-8
import sys,os
sys.path.append('../')

from django.db import models
# from django.contrib.contenttypes import generic
# from django.contrib.contenttypes.models import ContentType

from www.utils import random_file_name
from www import settings
import datasets.localdata
from ml_models.modelbase import *

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings") 
def get_upload_to(instance, filename):
    # paths = { 'I':'images/', 'V':'videos/', 'A':'audio/', 'D':'documents'/ }
    # return settings.MEDIA_ROOT + 'content/' + paths[instance.content_type] + filename
    return 'dataset/' + random_file_name(filename)
def get_model_upload_to(instance, filename):
    return settings.MEDIA_ROOT + 'upload/models/' + random_file_name(filename)

# null ：缺省设置为false.通常不将其用于字符型字段上，比如CharField,TextField上.字符型字段如果没有值会返回空字符串。
# blank：该字段是否可以为空。如果为假，则必须有值
# choices：一个用来选择值的2维元组。第一个值是实际存储的值，第二个用来方便进行选择。如SEX_CHOICES= ((‘F’,'Female’),(‘M’,'Male’),)
# core：db_column，db_index 如果为真将为此字段创建索引
# default：设定缺省值
# editable：如果为假，admin模式下将不能改写。缺省为真
# help_text：admin模式下帮助文档
# primary_key：设置主键，如果没有设置django创建表时会自动加上：

class Dataset(models.Model):
    id = models.AutoField(primary_key = True,)
    name = models.CharField(max_length=20)
    #if you use lambda here you can't pass migration, 因为lambda不能被序列化! 
    path = models.FileField(upload_to = get_upload_to)
    filetype = models.CharField(max_length=10)  
    head = models.CharField(max_length=1023, default='')
    attr_delim = models.CharField(max_length=3)
    record_delim = models.CharField(max_length=3)
    hashead = models.BooleanField(default=True)

    class Meta:
        db_table = 'dataset'

    def __unicode__(self):
        return "#{}: ({}) {} @ {} attr_delim: {} record_delim: {}".format(self.id,self.filetype,self.name,self.path,self.attr_delim,self.record_delim)

    @staticmethod
    def GetDatasets(pageindex = 0, max_item = 10):
        l = len(Dataset.objects.all())
        if l > 0:
            if max_item == -1:
                return Dataset.objects.all()
            else:
                return Dataset.objects.all()[min(pageindex*max_item,l-1):min((pageindex+1)*max_item,l)]
        else:
            return []
            
    @staticmethod
    def ViewDataset(unicodedatasetindex = None, maximum_items = 100):
        if unicodedatasetindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            datasetindex = int(unicodedatasetindex)
            if datasetindex >= 0:
                try:
                    datasetfile = Dataset.objects.get(id = datasetindex)
                    #open local dataset
                    lcdt = datasets.localdata.LocalData(datamapper = lambda data,colindex,head:int(data))
                    lcdt.ReadString(open(settings.MEDIA_ROOT+str(datasetfile.path),"r").read(), hasHead=True, getValue=True)
                    return lcdt
                except:
                    return None
        return None

    @staticmethod
    def DeleteDataset(unicodedatasetindex = None):
        if unicodedatasetindex != None:
            datasetindex = int(unicodedatasetindex)
            item = Dataset.objects.get(id = datasetindex)
            try:
                os.remove(settings.MEDIA_ROOT+str(item.path))
            except:
                pass
            item.delete()
            return 'true'
        return 'false'

class OnlineDataset(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=20)
    #if you use lambda here you can't pass migration, 因为lambda不能被序列化!
    head = models.CharField(max_length=1023, default='')
    url = models.CharField(max_length=200)
    location = models.CharField(max_length=1023)
    search = models.CharField(max_length=1023)
    renewstrategy = models.CharField(max_length=32)
    hashead = models.BooleanField(default=True)

    class Meta:
        db_table = 'onlinefield'

    def __unicode__(self):
        return "#{}: {} @ {} location: {} search: {}".format(self.id,self.name,self.url,self.location,self.search)

    @staticmethod
    def GetDatasets(pageindex = 0, max_item = 10):
        l = len(OnlineDataset.objects.all())
        if l > 0:
            if max_item == -1:
                return Dataset.objects.all()
            else:
                return OnlineDataset.objects.all()[min(pageindex*max_item,l-1):min((pageindex+1)*max_item,l)]
        else:
            return []
            
    @staticmethod
    def ViewDataset(unicodedatasetindex = None, maximum_items = 100):
        if unicodedatasetindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            datasetindex = int(unicodedatasetindex)
            try:
                olds = OnlineDataset.objects.get(id = datasetindex)
                ds = datasets.localdata.LocalData(online = True)
                ds.SetURL(olds.url, olds.location, None)
                ds.OnlineRenew()
                return ds
            except:
                return None
        return None

    @staticmethod
    def DeleteDataset(unicodedatasetindex = None):
        if unicodedatasetindex != None:
            datasetindex = int(unicodedatasetindex)
            item = OnlineDataset.objects.get(id = datasetindex)
            item.delete()
            return 'true'
        return 'false'

    @staticmethod
    def DumpDataset(unicodedatasetindex = None):
        if unicodedatasetindex != None:
            # try:
            datasetindex = int(unicodedatasetindex)
            filepath = 'dataset/' + random_file_name(None, 'txt')
            # DB
            olds = OnlineDataset.objects.get(id = datasetindex)
            print '-----------------------', olds
            ds = Dataset()
            ds.name = olds.name
            ds.path = filepath
            ds.filetype = 'TXT'
            ds.head = olds.head
            ds.hashead = olds.hashead
            ds.attr_delim = ',' 
            ds.record_delim = '\n' 
            ds.save()
            #file
            output = open(settings.MEDIA_ROOT + filepath, 'w')
            print '-----------------------', ds
            ds = OnlineDataset.ViewDataset(datasetindex)
            if ds == None:
                return 'false'
            output.write(','.join(ds.head) + '\n')
            for line in ds.items:
                output.write(','.join(line) + '\n')
            output.close()
            return 'true'
            # except:
            #     return 'false'
        return 'false'

    @staticmethod
    def AllRenewStrategies():
        return ['APPEND', 'REPLACE', 'COMPARE-APPEND']

class MLModel(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    '''
        INITED
        TRAINING
        TRAINED
    '''
    ModelTypeChoices = (
        ('INITED', 'INITED'),
        ('TRAINING', 'TRAINING'),
        ('TRAINED', 'TRAINED'),
    )
    modeltype = models.CharField(max_length = 32, choices = ModelTypeChoices)    
    modelstatus = models.CharField(max_length = 32)
    #if you use lambda here you can't pass migration, 因为lambda不能被序列化! 

    class Meta:
        db_table = 'models'

    @staticmethod
    def AllModelInfo():
        return ModelBase.AllModelInfo()

    @staticmethod
    def AllDistributedModels():
        return [ k  for (k,v) in MLModel.AllModelInfo().items() if v['distributed']==True ]
        return ["EM","SVM","NAIVE_BAYES","K_MEANS","KNN"]

    @staticmethod
    def AllNonTrainingModels():
        return [ k  for (k,v) in MLModel.AllModelInfo().items() if v['nontraining']==True]
        return ["MATRIX"]

    @staticmethod
    def AllModels():
        return [ k for (k,v) in MLModel.AllModelInfo().items()]
        return MLModel.AllDistributedModels() + ["DECISION_TREE","ADABOOST","PCA","LOGISTIC","CRF","FP_GROWTH"]            

    @staticmethod
    def GetModels(pageindex = 0, max_item = 10):
        l = len(MLModel.objects.all())
        if l > 0:
            return MLModel.objects.all()[min(pageindex*max_item,l-1):min((pageindex+1)*max_item,l)]
        else:
            return {}
            
    @staticmethod
    def ViewModel(unicodemodelindex = None, maximum_items = 100):
        if unicodemodelindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            modelindex = int(unicodemodelindex)
            try:
                md = MLModel.objects.get(id = modelindex)
                return md
            except:
                return None
        return None

    @staticmethod
    def DeleteModel(unicodemodelindex = None):
        if unicodemodelindex != None:
            modelindex = int(unicodemodelindex)
            item = MLModel.objects.get(id = modelindex)
            item.delete()
            return 'true'
        return 'false'

    def __unicode__(self):
        return "#{}: ({}) {} @ ".format(self.id,self.modeltype,self.name)

class TrainingTask(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    modeltype = models.CharField(max_length = 32) 
    #if you use lambda here you can't pass migration, 因为lambda不能被序列化! 

    class Meta:
        db_table = 'trainingtask'
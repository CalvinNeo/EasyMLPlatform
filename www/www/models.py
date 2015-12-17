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
from ml_models.model_task import *
from ml_models import *

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
    createtime = models.DateTimeField('create time', auto_now_add=True)

    class Meta:
        db_table = 'dataset'

    def __unicode__(self):
        return  "{{ 'id':{}, 'name':'{}', 'path':'{}' , 'filetype':'{}', 'head':'{}', 'attr_delim':'{}', 'record_delim':'{}', 'hashead':'{}' }}"\
            .format( str(self.id), str(self.name), str(self.path), str(self.filetype), str(self.head), 
                str(self.attr_delim), str(self.record_delim).replace('\n','\\\\n') , str(self.hashead))        
        return "#{}: ({}) {} @ {} attr_delim: {} record_delim: {}".format(self.id,self.filetype,self.name,self.path,self.attr_delim,self.record_delim)

    def __repr__(self):
        return  "{{ 'id':{}, 'name':'{}', 'path':'{}' , 'filetype':'{}', 'head':'{}', 'attr_delim':'{}', 'record_delim':'{}', 'hashead':'{}' }}"\
            .format( str(self.id), str(self.name), str(self.path), str(self.filetype), str(self.head), 
                str(self.attr_delim), str(self.record_delim).replace('\n','\\\\n') , str(self.hashead))

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
    def GetDataset(unicodedatasetindex = None):
        if unicodedatasetindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            datasetindex = int(unicodedatasetindex)
            if datasetindex >= 0:
                try:
                    dsinfo = Dataset.objects.get(id = datasetindex)
                    #open local dataset
                    lcdt = datasets.localdata.LocalData(datamapper = lambda data,colindex,head:int(data))
                    lcdt.ReadString(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
                    return {'info':dsinfo, 'view':lcdt}
                except:
                    return None
        return None

    @staticmethod
    def ViewDataset(unicodedatasetindex = None, maximum_items = 100):
        if unicodedatasetindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            datasetindex = int(unicodedatasetindex)
            if datasetindex >= 0:
                try:
                    datasetfile = Dataset.objects.get(id = datasetindex)
                    #open local dataset
                    lcdt = datasets.localdata.LocalData(datamapper = None)
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
    createtime = models.DateTimeField('create time', auto_now_add=True)

    class Meta:
        db_table = 'onlinefield'

    def __unicode__(self):
        return  "{{ 'id':{}, 'name':'{}', 'head':'{}' , 'url':'{}', 'location':'{}', 'search':'{}', 'renewstrategy':'{}', 'hashead':'{}' }}" \
            .format( str(self.id), str(self.name), str(self.head), str(self.url), str(self.location), 
                str(self.search), str(self.renewstrategy) , str(self.hashead))
        return "#{}: {} @ {} location: {} search: {}".format(self.id,self.name,self.url,self.location,self.search)

    def __repr__(self):
        return  "{{ 'id':{}, 'name':'{}', 'head':'{}' , 'url':'{}', 'location':'{}', 'search':'{}', 'renewstrategy':'{}', 'hashead':'{}' }}" \
            .format( str(self.id), str(self.name), str(self.head), str(self.url), str(self.location), 
                str(self.search), str(self.renewstrategy) , str(self.hashead))

    @staticmethod
    def GetDatasets(pageindex = 0, max_item = 10):
        l = len(OnlineDataset.objects.all())
        if l > 0:
            if max_item == -1:
                return OnlineDataset.objects.all()
            else:
                return OnlineDataset.objects.all()[min(pageindex*max_item,l-1):min((pageindex+1)*max_item,l)]
        else:
            return []

    @staticmethod
    def GetDataset(unicodedatasetindex = None):
        if unicodedatasetindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            datasetindex = int(unicodedatasetindex)
            if datasetindex >= 0:
                try:
                    olds = OnlineDataset.objects.get(id = datasetindex)
                    lcdt = datasets.localdata.LocalData(datamapper = None, online = True)
                except:
                    return None
                try:
                    lcdt.SetURL(olds.url, olds.location, None)
                    lcdt.OnlineRenew()
                    return {'info':olds, 'view':lcdt}
                except:
                    return {'info':olds, 'view':{}}
        return None

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
    createtime = models.DateTimeField('create time', auto_now_add=True)

    '''
        INITED
        TRAINING
        TRAINED
    '''
    ModelStatusChoices = (
        ('INITED', 'INITED'),
        ('TRAINING', 'TRAINING'),
        ('TRAINED', 'TRAINED'),
    )
    modeltype = models.CharField(max_length = 32)    
    modelstatus = models.CharField(max_length = 32, choices = ModelStatusChoices)

    DatasetPrototypeChoices = (
        ('LOCAL', 'LOCAL'),
        ('ONLINE', 'ONLINE'),
    )
    datasetprototype = models.CharField(max_length = 16, choices = DatasetPrototypeChoices)
    datasetindex = models.IntegerField()

    LossChoices = (
        ('QUAD','QUAD'),
        ('BIN','BIN'),
        ('ABS','ABS'),
        ('LOG','LOG'),
    )
    classfeatureindex = models.IntegerField() 
    loss = models.CharField(max_length = 20,default = 'QUAD',choices = LossChoices)
    # set default like this so that it can work with -1/1 and 0/1 
    positive = models.FloatField(default = 1.0)
    negative = models.FloatField(default = -0.5)

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
    def ViewModel(unicodemodelindex = None):
        if unicodemodelindex != None:
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
        return  "{{ 'id':{}, 'modeltype':'{}', 'name':'{}' }}".format( str(self.id), str(self.modeltype), str(self.name) ) 
        return "#{}: ({}) {} @ ".format(self.id,self.modeltype,self.name)

    def __repr__(self):
        return  "{{ 'id':{}, 'modeltype':'{}', 'name':'{}' }}".format( str(self.id), str(self.modeltype), str(self.name) ) 
        # return "#{}: ({}) {} @ ".format(self.id,self.modeltype,self.name)


class TrainingTask(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 20)
    modelprototype = models.CharField(max_length = 32) 
    modelindex = models.IntegerField()
    createtime = models.DateTimeField('create time', auto_now_add=True)
    #if you use lambda here you can't pass migration, 因为lambda不能被序列化! 

    class Meta:
        db_table = 'trainingtask'

    @staticmethod
    def GetTasks(pageindex = 0, max_item = 10):
        l = len(TrainingTask.objects.all())
        if l > 0:
            if max_item == -1:
                return TrainingTask.objects.all()
            else:
                return TrainingTask.objects.all()[min(pageindex*max_item,l-1):min((pageindex+1)*max_item,l)]
        else:
            return []

    @staticmethod
    def CreateTrain(unicodemodelindex = None):
        '''
            md: MLModel
            tt: TrainingTask
            mlmd: ModelRunTask
        '''
        if unicodemodelindex != None:
            modelindex = int(unicodemodelindex)
            md = MLModel.objects.get(id = modelindex)
            if md != None:
                # New Task
                tt = TrainingTask()
                tt.name = ''
                tt.modelprototype = md.modeltype
                tt.modelindex = modelindex
                tt.save()
                # Modify Model Record
                md.modelstatus = 'TRAINING'
                md.save()
                # Open dataset
                # Create Machine Learning Instance
                # Get TrainingTask id
                mlmd = ModelRunTask(TrainingTask.objects.all()[len(TrainingTask.objects.all())-1].id, md)
                
                return 'true'
            return 'false'

    @staticmethod
    def StartTrain(unicodetaskindex = None):
        pass


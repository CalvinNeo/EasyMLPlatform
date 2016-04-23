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

'''
    变量名解释：
    ds: 包含dsinfo和dsview/dataset两部分，结构为{'info': dsinfo, 'view': dataset}
    dataset(oldataset): 是一个LocalDataset
    dsinfo(oldsinfo): 是Table里面的一个Record，记录数据集信息
    mdinfo: 是Table里面的一个Record，记录模型信息
    md: 一个ModelBase对象
    datasets: 是一个模块，里面有LocalData等类
    Dataset: 是www.models.Dataset
    MLModel: 是www.models.MLModel
'''

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
    user = models.CharField(max_length=20)
    group = models.CharField(max_length=20)

    class Meta:
        db_table = 'dataset'

    def __unicode__(self):
        return  "{{ 'id':{}, 'name':'{}', 'path':'{}' , 'filetype':'{}', 'head':'{}', 'attr_delim':'{}', 'record_delim':'{}', 'hashead':'{}' }}"\
            .format( str(self.id), str(self.name), str(self.path), str(self.filetype), str(self.head), 
                str(self.attr_delim), str(self.record_delim).replace('\n','\\\\n') , str(self.hashead))        

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
                return Dataset.objects.all()[min(pageindex*max_item, l-1): min((pageindex+1)*max_item, l)]
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
                    dataset = datasets.localdata.LocalData(datamapper = None)
                    if dsinfo.filetype == 'TXT' or dsinfo.filetype == 'CSV':
                        dataset.ReadString(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
                    elif dsinfo.filetype == 'XML':
                        dataset.ReadXML(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
                    elif dsinfo.filetype == 'XLS':
                        dataset.ReadXLS(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
                    return {'info':dsinfo, 'view':dataset}
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
                    dsinfo = Dataset.objects.get(id = datasetindex)
                    #open local dataset
                    dataset = datasets.localdata.LocalData(datamapper = None)
                    if dsinfo.filetype == 'TXT' or dsinfo.filetype == 'CSV':
                        dataset.ReadString(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
                    elif dsinfo.filetype == 'XML':
                        dataset.ReadXML(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
                    elif dsinfo.filetype == 'XLS':
                        dataset.ReadXLS(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
                    return dataset
                except:
                    return None
        return None

    @staticmethod
    def DeleteDataset(unicodedatasetindex = None):
        if unicodedatasetindex != None:
            datasetindex = int(unicodedatasetindex)
            dsinfo = Dataset.objects.get(id = datasetindex)
            try:
                os.remove(settings.MEDIA_ROOT+str(dsinfo.path))
            except:
                pass
            dsinfo.delete()
            return 'true'
        return 'false'

    @staticmethod
    def GetImage(unicodedatasetindex = None):
        dsinfo = None
        if unicodedatasetindex != None:
            datasetindex = int(unicodedatasetindex)
            dsinfo = Dataset.objects.get(id = datasetindex)
        if dsinfo != None:
            #open local dataset
            dataset = datasets.localdata.LocalData(datamapper = None)
            if dsinfo.filetype == 'TXT' or dsinfo.filetype == 'CSV':
                dataset.ReadString(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
            elif dsinfo.filetype == 'XML':
                dataset.ReadXML(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
            elif dsinfo.filetype == 'XLS':
                dataset.ReadXLS(open(settings.MEDIA_ROOT+str(dsinfo.path),"r").read(), hasHead=True, getValue=True)
            image = dataset.Graph('')
            return image
        return ''

class OnlineDataset(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=20)
    #if you use lambda here you can't pass migration, 因为lambda不能被序列化!
    head = models.CharField(max_length=1023, default='')
    url = models.CharField(max_length=200)
    location = models.CharField(max_length=1023)
    search = models.CharField(max_length=1023)
    renewstrategy = models.CharField(max_length=32)
    metatype = models.CharField(max_length=32)
    hashead = models.BooleanField(default=True)
    createtime = models.DateTimeField('create time', auto_now_add=True)
    user = models.CharField(max_length=20)
    group = models.CharField(max_length=20)

    class Meta:
        db_table = 'onlinefield'

    def __unicode__(self):
        return  "{{ 'id':{}, 'name':'{}', 'head':'{}' , 'url':'{}', 'location':'{}', 'search':'{}', 'renewstrategy':'{}', 'hashead':'{}' }}" \
            .format( str(self.id), str(self.name), str(self.head), str(self.url), str(self.location), 
                str(self.search), str(self.renewstrategy) , str(self.hashead))

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
                    oldsinfo = OnlineDataset.objects.get(id = datasetindex)
                    oldataset = datasets.localdata.LocalData(datamapper = None, online = True, renewstrategy = oldsinfo.renewstrategy)
                except:
                    return None
                # try:
                if oldsinfo.metatype == 'HTML':
                    oldataset.SetURL(oldsinfo.url, oldsinfo.location, None)
                elif oldsinfo.metatype == 'JSON':
                    oldataset.SetJSON(oldsinfo.url)
                elif oldsinfo.metatype == 'CSV':
                    oldataset.SetCSV(oldsinfo.url)
                elif oldsinfo.metatype == 'XML':
                    pass
                # renew when set
                # oldataset.OnlineRenew()
                return {'info':oldsinfo, 'view':oldataset}
                # except:
                #     return {'info':oldsinfo, 'view':{}}
        return None

    @staticmethod
    def ViewDataset(unicodedatasetindex = None, maximum_items = 100):
        if unicodedatasetindex != None:
            #index不是从1严格递增的,可能是1,3,9这样的,因为数据集会被删除
            datasetindex = int(unicodedatasetindex)
            # try:
            oldsinfo = OnlineDataset.objects.get(id = datasetindex)
            oldataset = datasets.localdata.LocalData(datamapper = None, online = True)
            if oldsinfo.metatype == 'HTML':
                oldataset.SetURL(oldsinfo.url, oldsinfo.location, None)
            elif oldsinfo.metatype == 'JSON':
                oldataset.SetJSON(oldsinfo.url)
            elif oldsinfo.metatype == 'CSV':
                oldataset.SetCSV(oldsinfo.url)
            elif oldsinfo.metatype == 'XML':
                pass
            oldataset.OnlineRenew()
            return oldataset
            # except:
            #     return None
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
            oldsinfo = OnlineDataset.objects.get(id = datasetindex)
            dsinfo = Dataset()
            dsinfo.name = oldsinfo.name
            dsinfo.path = filepath
            dsinfo.filetype = 'TXT'
            dsinfo.head = oldsinfo.head
            dsinfo.hashead = oldsinfo.hashead
            dsinfo.attr_delim = ',' 
            dsinfo.record_delim = '\n' 
            dsinfo.save()
            #file
            output = open(settings.MEDIA_ROOT + filepath, 'w')
            oldataset = OnlineDataset.ViewDataset(datasetindex)
            if oldataset == None:
                return 'false'
            output.write(','.join(map(str, oldataset.head)) + '\n')
            for line in oldataset.items:
                output.write(','.join(map(str, line)) + '\n')
            output.close()
            return 'true'
            # except:
            #     return 'false'
        return 'false'

    @staticmethod
    def GetImage(unicodedatasetindex = None):
        oldsinfo = None
        if unicodedatasetindex != None:
            datasetindex = int(unicodedatasetindex)
            oldsinfo = OnlineDataset.objects.get(id = datasetindex)
        if oldsinfo != None:
            # set online dataset
            oldataset = datasets.localdata.LocalData(datamapper = None, online = True)
            if oldsinfo.metatype == 'HTML':
                oldataset.SetURL(oldsinfo.url, oldsinfo.location, None)
            elif oldsinfo.metatype == 'JSON':
                oldataset.SetJSON(oldsinfo.url)
            elif oldsinfo.metatype == 'CSV':
                oldataset.SetCSV(oldsinfo.url)
            elif oldsinfo.metatype == 'XML':
                pass
            image = oldataset.Graph('')
            return image
        return ''

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
    '''
        注意到Dataset和MLModel都有classfeatureindex字段，区别如下：
        Dataset里面的classfeature字段是在训练阶段取的MLModel的classfeatureindex值
    '''
    classfeatureindex = models.IntegerField() 
    loss = models.CharField(max_length = 20, default = 'QUAD', choices = LossChoices)
    # set default like this so that it can work with -1/1 and 0/1 
    positive = models.FloatField(default = 1.0)
    negative = models.FloatField(default = -0.5)
    model_path = models.CharField(max_length = 255)

    #if you use lambda here you can't pass migration, 因为lambda不能被序列化! 

    class Meta:
        db_table = 'models'

    @staticmethod
    def AllModelInfo():
        return ModelBase.AllModelInfo()

    @staticmethod
    def AllDistributedModels():
        return [ k  for (k,v) in MLModel.AllModelInfo().items() if v['distributed']==True ]

    @staticmethod
    def AllNonTrainingModels():
        return [ k  for (k,v) in MLModel.AllModelInfo().items() if v['nontraining']==True]

    @staticmethod
    def AllModels():
        return [ k for (k,v) in MLModel.AllModelInfo().items()]
    
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
                mdinfo = MLModel.objects.get(id = modelindex)
                return mdinfo
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

    @staticmethod
    def GetImage(unicodemodelindex = None):
        mlmd = None
        if unicodemodelindex != None:
            modelindex = int(unicodemodelindex)
            mlmd = MLModel.objects.get(id = modelindex)
        if mlmd != None:
            clsname = mlmd.modeltype
            if (clsname.upper() in ModelBase.AllModelInfo().keys()):
                md = ModelBase.AllModelInfo()[clsname.upper()]['cls'](LocalData())
                md.Load(mlmd.model_path)
                image = md.Graph('')
                return image
        return ''

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

    # def __unicode__(self):
    #     return  "{{ 'id':{}, 'modeltype':'{}', 'name':'{}', 'createtime':'{}', 'modelindex':'{}' }}".format( str(self.id), str(self.modelprototype), str(self.name), str(self.createtime), str(self.modelindex) ) 

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
    def DeleteTask(unicodetaskindex = None):
        if unicodetaskindex != None:
            taskindex = int(unicodetaskindex)
            item = TrainingTask.objects.get(id = taskindex)
            item.delete()
            return 'true'
        return 'false'


    @staticmethod
    def CreateTrain(unicodemodelindex = None):
        '''
            mdinfo: MLModel
            traintask: TrainingTask
            mdruntask: ModelRunTask
        '''
        if unicodemodelindex != None:
            modelindex = int(unicodemodelindex)
            mdinfo = MLModel.objects.get(id = modelindex)
            if mdinfo != None:
                # New Task in DB model
                traintask = TrainingTask()
                traintask.name = ''
                traintask.modelprototype = mdinfo.modeltype
                traintask.modelindex = modelindex
                traintask.save()
                # Modify Model Record
                mdinfo.modelstatus = 'TRAINING'
                mdinfo.save()
                # Open dataset on db
                if mdinfo.datasetprototype == 'LOCAL':
                    dsinfo = Dataset.GetDataset(mdinfo.datasetindex) 
                else:
                    dsinfo = OnlineDataset.GetDataset(mdinfo.datasetindex)
                # Create Machine Learning Instance
                # Get TrainingTask id
                mdruntask = ModelRunTask(TrainingTask.objects.all()[len(TrainingTask.objects.all())-1].id, mdinfo, dsinfo)
                mdruntask.Start()

                # now Training is over
                mdinfo.modelstatus = 'TRAINED'
                # save training result
                mdinfo.model_path = 'cache/models/'+random_file_name(None,'trd')
                mdruntask.Save(mdinfo.model_path)
                mdinfo.save()
                traintask.delete()
                
                return 'true'
            return 'false'

    @staticmethod
    def StartTrain(unicodetaskindex = None):
        pass

class ApplyTask(models.Model):

    id = models.AutoField(primary_key = True)

    class Meta:
        db_table = 'applyingtask'

    @staticmethod
    def CreateApply(unicodemodelindex = None, unicodedatasetindex = None
        , unicodeoldatasetindex = None, unicodeselectwhichdatasettype = 'ds'
        , unicoderemove = ''):
        if unicodemodelindex != None:
            modelindex = int(unicodemodelindex)
            mdinfo = MLModel.objects.get(id = modelindex)
        if str(unicodeselectwhichdatasettype) == 'ds':
            dsinfo = Dataset.GetDataset(int(unicodedatasetindex))
        else:
            dsinfo = OnlineDataset.GetDataset(int(unicodeoldatasetindex))
        mlmd = ModelApplyTask(0, 
            mdinfo, dsinfo)
            #, None if str(unicoderemove)=='' else int(unicoderemove))
        return mlmd

class AssessTask(models.Model):

    id = models.AutoField(primary_key = True)

    class Meta:
        db_table = 'assesstask'

    @staticmethod
    def CreateAssess(unicodemodelindex = None, unicodedatasetindex = None
        , unicodeoldatasetindex = None, unicodeselectwhichdatasettype = 'ds'
        , unicodeclassfeatureindex = -1, unicodeassessmethod = 'sfold'):
        if unicodemodelindex != None:
            modelindex = int(unicodemodelindex)
            mdinfo = MLModel.objects.get(id = modelindex)
        if str(unicodeselectwhichdatasettype) == 'ds':
            dsinfo = Dataset.GetDataset(int(unicodedatasetindex))
        else:
            dsinfo = OnlineDataset.GetDataset(int(unicodeoldatasetindex))
        mlmd = ModelAssessTask(0, mdinfo, dsinfo, str(unicodeassessmethod), -1) # unicodeclassfeatureindex is deprecated
        return mlmd


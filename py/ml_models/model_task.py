#coding:utf8
import sys
sys.path.append('..')

from modelbase import ModelBase
import datasets.localdata
from datasets.monads import *
from datasets.localdata import *
import itertools
from ml_models import *

class ModelRunTask:
    def __init__(self, taskid, mdinfo, ds):
        '''
            Instance and run Model according to given `model` and `dataset`

            mdinfo is a MLModel object(Database record)
            ds is {'info':dsinfo, 'view':dataset} or {'info':oldsinfo, 'view':dataset} while 
                dbds and oldsds is Dataset or OnlineDataset object
                lcdt is datasets.localdata.LocalData object
        '''
        clsname = mdinfo.modeltype
        # possibles = globals()
        # possibles.update(locals())
        if (clsname.upper() in ModelBase.AllModelInfo().keys()): # and (clsname in possibles.keys()):
            # dataset.classfeatureindex is determined by mdinfo(and when training md.classfeatureindex is determined by dataset.classfeatureindex)
            ds['view'].classfeatureindex = mdinfo.classfeatureindex

            # need to set args to __init__
            # md = possibles.get(clsname)(dataset = ds['view'])
            # print ModelBase.AllModelInfo()[clsname.upper()]
            md = ModelBase.AllModelInfo()[clsname.upper()]['cls'](dataset = ds['view'])
            md.positive = mdinfo.positive
            md.negative = mdinfo.negative
            md.classfeatureindex = mdinfo.classfeatureindex
            md.loss = {
                'QUAD': ModelBase.QuadLoss
                ,'BIN': ModelBase.BinLoss
                ,'ABS': ModelBase.AbsLoss
                ,'LOG': ModelBase.LogLoss
            }[mdinfo.loss]

            self.dataset = ds['view']
            self.model = md

    def Start(self):
        '''
            Called by /www/models.py
        '''
        self.model.Train()

    def Save(self, name):
        '''
            Called by /www/models.py
        '''
        self.model.Save(name)

    def Load(self, name):
        '''
            Called by /www/models.py
        '''
        self.model.Load(name)


class ModelApplyTask:
    def __init__(self, taskid, mdinfo, ds):
        clsname = mdinfo.modeltype
        if (clsname.upper() in ModelBase.AllModelInfo().keys()): 
            # dataset.classfeatureindex is determined by mdinfo(and when training md.classfeatureindex is determined by dataset.classfeatureindex)
            ds['view'].classfeatureindex = mdinfo.classfeatureindex

            md = ModelBase.AllModelInfo()[clsname.upper()]['cls'](dataset = ds['view'])

            self.dataset = ds['view']
            self.model = md
            self.Load(mdinfo.model_path)

    def Start(self):
        '''
            Called by /www/models.py
        '''
        return self.model.Apply(self.dataset)

    def Save(self, name):
        '''
            Called by /www/models.py
        '''
        self.model.Save(name)

    def Load(self, name):
        '''
            Called by /www/models.py
        '''
        self.model.Load(name)

class ModelAssessTask:
    def __init__(self, taskid, mdinfo, ds, method, classfeatureindex = None):
        '''
            classfeatureindex和训练得到的模型是紧密相关的，对classfeatureindex的改动会牵涉到对模型的改动，因此classfeatureindex一定要去db_model的classfeatureindex
        '''
        clsname = mdinfo.modeltype
        if (clsname.upper() in ModelBase.AllModelInfo().keys()): 

            # dataset is load from Dataset.GetDataset
            ds['view'].classfeatureindex = mdinfo.classfeatureindex

            md = ModelBase.AllModelInfo()[clsname.upper()]['cls'](dataset = ds['view'])

            self.dataset = ds['view']
            self.model = md
            self.Load(mdinfo.model_path)

            self.assessmodel = assessment.Assessment(self.model, self.dataset)

    def Start(self):
        '''
            Called by /www/models.py
        '''
        if self.assessmodel.Protoclass == "CLASSIFY":
            self.assessmodel.TFPN()
        elif self.Protoclass == "REGRESS":
            self.assessmodel.assessmodel.Loss()
        elif self.assessmodel.Protoclass == "CLUSTER":
            pass
        else:
            pass
        return self.assessmodel
        
    def Save(self, name):
        '''
            Called by /www/models.py
        '''
        self.model.Save(name)

    def Load(self, name):
        '''
            Called by /www/models.py
        '''
        self.model.Load(name)

if __name__ == '__main__':
    possibles = globals()
    print possibles.keys()
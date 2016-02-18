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
    def __init__(self, taskid, db_model, dataset):
        '''
            Instance and run Model according to given `model` and `dataset`

            db_model is a MLModel object
            dataset is {'info':dbds, 'view':lcdt} or {'info':oldbds, 'view':lcdt} while 
                dbds and oldsds is Dataset or OnlineDataset object
                lcdt is datasets.localdata.LocalData object
        '''
        clsname = db_model.modeltype
        # print ")))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))0",db_model.modeltype, clsname.upper(),clsname.upper() in ModelBase.AllModelInfo().keys()
        # possibles = globals()
        # possibles.update(locals())
        if (clsname.upper() in ModelBase.AllModelInfo().keys()): # and (clsname in possibles.keys()):
            # dataset
            dataset['view'].classfeatureindex = db_model.classfeatureindex

            # need to set args to __init__
            # md = possibles.get(clsname)(dataset = dataset['view'])
            # print ModelBase.AllModelInfo()[clsname.upper()]
            md = ModelBase.AllModelInfo()[clsname.upper()]['cls'](dataset = dataset['view'])
            md.positive = db_model.positive
            md.negative = db_model.negative
            md.classfeatureindex = db_model.classfeatureindex
            md.loss = {
                'QUAD': ModelBase.QuadLoss
                ,'BIN': ModelBase.BinLoss
                ,'ABS': ModelBase.AbsLoss
                ,'LOG': ModelBase.LogLoss
            }[db_model.loss]

            self.dataset = dataset['view']
            self.model = md

            print dataset,md

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
    def __init__(self, taskid, db_model, dataset):
        clsname = db_model.modeltype
        if (clsname.upper() in ModelBase.AllModelInfo().keys()): 
            # dataset
            dataset['view'].classfeatureindex = db_model.classfeatureindex

            md = ModelBase.AllModelInfo()[clsname.upper()]['cls'](dataset = dataset['view'])

            self.dataset = dataset['view']
            self.model = md
            print db_model.model_path
            self.Load(db_model.model_path)

            print dataset,md

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

if __name__ == '__main__':
    possibles = globals()
    print possibles.keys()
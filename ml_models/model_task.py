#coding:utf8
import sys
sys.path.append('..')

from modelbase import ModelBase
import datasets.localdata
from datasets.monads import *
import itertools
from ml_models import *

class ModelRunTask:
    def __init__(self, taskid, db_model):
        '''
            Instance and run Model according to given `model` and `dataset`

            db_model is a MLModel object
            dataset is {'info':dbds, 'view':lcdt} or {'info':oldbds, 'view':lcdt} while 
                dbds and oldsds is Dataset or OnlineDataset object
                lcdt is datasets.localdata.LocalData object
        '''
        clsname = db_model.modeltype
        if clsname.upper in ModelBase.AllModelInfo().keys():
            possibles = globals()
            possibles.update(locals())
            if clsname in possibles.keys():
                # dataset
                if db_model.datasetprototype == 'LOCAL':
                    dbds = Dataset.GetDataset(db_model.datasetindex)
                else:
                    dbds = OnlineDataset.GetDataset(db_model.datasetindex)
                dbds.classfeatureindex = db_model.classfeatureindex

                # need to set args to __init__
                md = possibles.get(clsname)(dataset = dataset['view'])
                md.positive = db_model.positive
                md.negative = db_model.negative
                md.classfeatureindex = db_model.classfeatureindex
                md.loss = {
                    'QUAD': ModelBase.QuadLoss
                    ,'BIN': ModelBase.BinLoss
                    ,'ABS': ModelBase.AbsLoss
                    ,'LOG': ModelBase.LogLoss
                }[db_model.loss]

if __name__ == '__main__':
    possibles = globals()
    print possibles.keys()
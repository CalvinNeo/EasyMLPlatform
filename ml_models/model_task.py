#coding:utf8
import sys
sys.path.append('..')

from modelbase import ModelBase
import datasets.localdata
from datasets.monads import *
import itertools
from ml_models import *

class ModelRunTask:
    def __init__(self, taskid, db_models, dataset):    
        clsname = db_models.modeltype
        if clsname.upper in ModelBase.AllModelInfo().keys():
            possibles = globals()
            possibles.update(locals())
            if clsname in possibles.keys():
                # need to set args to __init__
                md = possibles.get(clsname)()

if __name__ == '__main__':
    possibles = globals()
    print possibles.keys()
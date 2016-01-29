#coding:utf8
import sys
sys.path.append('..')

from modelbase import *
import numpy as np
import math
import pylab as pl
from collections import defaultdict, namedtuple
import itertools

class NaiveBayes(ModelBase):
    def __init__(self, dataset, *args, **kwargs):
        '''
            dataset: (datasets.localdata) 
            classfeatureindex: index of the column which defines the feature in dataset 
        '''
        ModelBase.__init__(self, dataset, 'CLASSIFY', *args, **kwargs)
        # self.Test = self.Classify
        # self.Train = self.CreateTree

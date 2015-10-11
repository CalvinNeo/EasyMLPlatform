#coding:utf8
import sys
sys.path.append('..')

import math
import datasets.localdata
import operator
import numpy as np
import sys
from collections import defaultdict, namedtuple
import itertools

class LogisticRegression:
    def __init__(self, dataset, classfeatureindex = -1):
        self.dataset = dataset
        self.classfeatureindex = classfeatureindex #index of the column which defines the feature in dataset
        self.sigmoid = lambda x: 1 / (1 + math.e ** (-x))
    def Regress(self):
        data = np.matrix(self.dataset.items)
    def GradAscent(self):
        pass
if __name__ == '__main__':
    def my_mapper(data, colindex, head):
        if head == 'water':
            return int(data)
        elif head == 'foot':
            return int(data)
        else:
            return str(data)
    ld = datasets.localdata.LocalData()
    ld.ReadString(open("dat_cls.txt","r").read(),True,mapper=my_mapper)
    dt = LogisticRegression(ld,-1)
    dt.Regress()
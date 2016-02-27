#coding:utf8
import sys
sys.path.append('..')

from modelbase import ModelBase
import math
import datasets.localdata
from datasets.monads import *
import operator
import numpy as np
from collections import defaultdict, namedtuple
import itertools
import pickle

class LogisticRegression(ModelBase):
    '''
        simple Logistic Regression is linear
    '''
    def __init__(self, dataset, classfeatureindex = -1, alpha = 0.01, maxiter = 500):
        ModelBase.__init__(self, dataset, 'LOGISTIC', *args, **kwargs)
        self.classfeatureindex = classfeatureindex #index of the column which defines the feature in dataset
        self.Test = self.Classify
        self.Apply = self.ClassifyDataset
        self.Train = self.Regress
        self.Save = self.DumpLogistic
        self.Load = self.LoadLogistic
        self.Graph = self.ShowImage
        # use default
        # self.T = self.RealValue
        self.tree = {}

        self.sigmoid = lambda input_n:np.vectorize(lambda n: 1.0/(1.0+math.e**(-n)))(input_n)
        self.alpha = alpha
        self.maxiter = maxiter
        self.weights = np.ones((len(self.dataset.head),1))
        self.classfeatureindex = self.dataset.classfeatureindex

    def Regress(self):
        data = np.matrix([item[:self.classfeatureindex] + item[self.classfeatureindex+1:] + [1] if self.classfeatureindex > -1 else item[:len(item)-1] + [1] for item in self.dataset.items])
        t = np.matrix([item[self.classfeatureindex] for item in self.dataset.items]).T
        itemcount, featurecount = data.shape
        self.weights = np.ones((featurecount,1)) * 1 # featurecount 个 feature + 1 个常量
        for itertime in xrange(self.maxiter):
            a = self.sigmoid(np.dot(data, self.weights))
            e = t - a
            self.weights += self.alpha * np.dot(data.T, e)

    def Classify(self, test):
        p = np.matrix(test + [1] )
        print self.sigmoid(np.dot(p , self.weights))
        return 1.0 if self.sigmoid(np.dot(p, self.weights)) > 0.5 else 0.0

    def ClassifyDataset(self, dataset, remove_item = None):
        '''
            predict a series sample inputs from a dataset
        '''
        resultdataset = LocalData(None, head = self.dataset.head+['result'], classfeatureindex = -1)
        for item in dataset.Iter():
            resultdataset.items.append(item+[self.Classify(item)])
        return resultdataset

    def DumpLogistic(self):
        fw = open(filename, 'w')
        pickle.dump(self.weights, fw)
        fw.close()

    def LoadLogistic(self):
        fr = open(filename)
        self.weights = pickle.load(fr)

    def ShowImage(self):
        pass

    def RealValue(self):
        pass

if __name__ == '__main__':
    def my_mapper(data, colindex, head):
        if head == 'water':
            return float(data)
        elif head == 'foot':
            return float(data)
        else:
            if data == 'yes':
                return 1.0
            else:
                return 0.0
                
    ld = datasets.localdata.LocalData(datamapper = my_mapper)
    ld.ReadString(open("dat_cls.txt","r").read(),True)
    dt = LogisticRegression(ld, -1, maxiter = 100, alpha = 0.01)
    dt.Regress()
    print "[1,1]", dt.Classify([1.0,1.0])
    print "[0,1]", dt.Classify([0.0,1.0])
    print "[1,0]", dt.Classify([1.0,0.0])
    print "[0,0]", dt.Classify([0.0,0.0])
    # print "[1,1]", dt.Classify([1.0,1.0])
    # print "[0,1]", dt.Classify([-1.0,1.0])
    # print "[1,0]", dt.Classify([1.0,-1.0])
    # print "[0,0]", dt.Classify([-1.0,-1.0])
    print "weight",dt.weights

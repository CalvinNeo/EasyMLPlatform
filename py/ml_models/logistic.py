#coding:utf8
import sys
sys.path.append('..')

from modelbase import ModelBase
import math
import datasets
from datasets.localdata import *
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
    def __init__(self, dataset, classfeatureindex = -1, alpha = 0.2, maxiter = 50, *args, **kwargs):
        ModelBase.__init__(self, dataset, 'LOGISTIC', *args, **kwargs)
        self.classfeatureindex = classfeatureindex #index of the column which defines the feature in dataset
        self.Test = self.Classify2
        self.Apply = self.ClassifyDataset
        self.Train = self.Regress
        self.Save = self.DumpLogistic
        self.Load = self.LoadLogistic
        self.Graph = self.ShowImage
        self.Positive = 1
        self.Negative = -1
        # use default
        # self.T = self.RealValue
        self.tree = {}

        self.sigmoid = lambda input_n:np.vectorize(lambda n: 1.0/(1.0+math.e**(-n)))(input_n)
        self.alpha = alpha
        self.maxiter = maxiter
        self.weights = np.ones((len(self.dataset.head),1))
        self.classfeatureindex = self.dataset.classfeatureindex

    def Regress(self):
        data = np.matrix([item[:self.classfeatureindex] + [0] + item[self.classfeatureindex+1:]  if self.classfeatureindex > -1 else item[:len(item)-1] + [0] for item in self.dataset.Iter()])
        t = np.matrix([item[self.classfeatureindex] for item in self.dataset.Iter()]).T
        itemcount, featurecount = data.shape
        self.weights = np.ones((featurecount,1)) * 1 # featurecount 个 feature + 1 个常量
        print self.weights
        for itertime in xrange(self.maxiter):
            a = self.sigmoid(np.dot(data, self.weights))
            e = t - a
            self.weights += self.alpha * np.dot(data.T, e)

    def Classify(self, test):
        # p = np.matrix(test[:self.classfeatureindex] + test[self.classfeatureindex+1:] + [1] if self.classfeatureindex > -1 else test + [1] )
        # p = np.matrix(test + [1] )
        p = np.matrix(test)
        # print self.sigmoid(np.dot(p , self.weights))
        return self.Positive if self.sigmoid(np.dot(p, self.weights)) > (self.Positive + self.Negative) / 2.0 else self.Negative

    def Classify2(self, test):
        '''
            predict a single new sample input with trained logistic
        '''
        p = np.matrix(test[:self.classfeatureindex] + [1] + test[self.classfeatureindex + 1:]  if self.classfeatureindex > -1 else test + [1] )
        return self.Positive if self.sigmoid(np.dot(p, self.weights)) > (self.Positive + self.Negative) / 2.0 else self.Negative

    def ClassifyDataset(self, dataset, remove_item = None):
        '''
            predict a series sample inputs from a dataset
        '''
        resultdataset = LocalData(None, head = self.dataset.head + ['result'], classfeatureindex = -1)
        for item in dataset.Iter():
            # resultdataset.items.append(item + [self.Classify(item + [1])])
            resultdataset.items.append(item + [self.Classify2(item)])
        return resultdataset

    def DumpLogistic(self, filename):
        fw = open(filename, 'w')
        pickle.dump(self.weights, fw)
        fw.close()

    def LoadLogistic(self, filename):
        fr = open(filename)
        self.weights = pickle.load(fr)

    def ShowImage(self, op):
        pass

    def RealValue(self):
        pass

if __name__ == '__main__':
               
    ld = datasets.localdata.LocalData()
    ld.ReadString(open("iris.txt","r").read(), True)
    dt = LogisticRegression(ld, -1, maxiter = 50, alpha = 0.01)
    dt.Regress()
    print "weight",dt.weights
    print "1", dt.Classify2([5.1,3.7,1.5,0.4])
    print "-1", dt.Classify2([6.3,2.5,4.9,1.5])

    # print "[1,1]", dt.Classify([1.0,1.0])
    # print "[0,1]", dt.Classify([0.0,1.0])
    # print "[1,0]", dt.Classify([1.0,0.0])
    # print "[0,0]", dt.Classify([0.0,0.0])

    # print "[1,1]", dt.Classify([1.0,1.0])
    # print "[0,1]", dt.Classify([-1.0,1.0])
    # print "[1,0]", dt.Classify([1.0,-1.0])
    # print "[0,0]", dt.Classify([-1.0,-1.0])

#coding:utf8
import sys
sys.path.append('..')

from modelbase import *
import math
import datasets.localdata
from datasets.monads import *
import operator
import numpy as np
import sys
from collections import defaultdict, namedtuple
import itertools

class LogisticRegression:
    '''
        simple Logistic Regression is linear
    '''
    def __init__(self, dataset, classfeatureindex = -1, alpha = 0.01, maxiter = 500):
        self.dataset = dataset
        self.classfeatureindex = classfeatureindex #index of the column which defines the feature in dataset
        self.sigmoid = lambda input_n:np.vectorize(lambda n: 1.0/(1.0+math.e**(-n)))(input_n)
        self.alpha = alpha
        self.maxiter = maxiter
        self.weights = np.ones((len(self.dataset.head),1))

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

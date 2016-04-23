#coding:utf8
import sys
sys.path.append('..')

import math
from modelbase import *
import datasets
from datasets.localdata import *
from datasets.monads import *
import operator
import json
import pickle
import itertools
import numpy as np
from sklearn import metrics
from sklearn.naive_bayes import GaussianNB


class NaiveBayes(ModelBase):
    def __init__(self, dataset, *args, **kwargs):
        '''
            dataset: (datasets.localdata) 
            classfeatureindex: index of the column which defines the feature in dataset 
        '''
        ModelBase.__init__(self, dataset, 'NAIVE_BAYES', *args, **kwargs)
        self.Test = self.Classify2
        self.Apply = self.ClassifyDataset
        self.Train = self.NaiveBayes
        self.Save = self.Dump
        self.Load = self.LoadFromFile
        self.Graph = self.ShowImage
        # use default
        # self.T = self.RealValue
        self.model = GaussianNB()

    def NaiveBayes(self):
        X = np.matrix([item[:self.classfeatureindex] + [0] + item[self.classfeatureindex+1:]  if self.classfeatureindex > -1 else item[:len(item)-1] + [0] for item in self.dataset.Iter()])
        y = np.array([item[self.classfeatureindex] for item in self.dataset.Iter()])
        self.model.fit(X, y)

    def Classify2(self, test):
        '''
            predict a single new sample input with trained naive bayes
        '''
        p = np.matrix(test[:self.classfeatureindex] + [1] + test[self.classfeatureindex + 1:]  if self.classfeatureindex > -1 else test + [1] )
        r = self.model.predict(p)
        return r

    def ClassifyDataset(self, dataset, remove_item = None):
        '''
            predict a series sample inputs from a dataset
        '''
        resultdataset = LocalData(None, head = self.dataset.head + ['result'], classfeatureindex = -1)
        for item in dataset.Iter():
            # resultdataset.items.append(item + [self.Classify(item + [1])])
            resultdataset.items.append(item + [self.Classify2(item)])
        return resultdataset

    def Dump(self, filename):
        fw = open(filename, 'w')
        pickle.dump(self.model, fw)
        fw.close()

    def LoadFromFile(self, filename):
        fr = open(filename)
        self.model = pickle.load(fr)

    def ShowImage(self, op):
        pass
        # tr = GraphTree()
        # # JSON can't have non-string key
        # tr.load(self.tree)
        # return tr.createPlot(show = False)

    def RealValue(self, op):
        pass

if __name__ == '__main__':
    ld = datasets.localdata.LocalData(classfeatureindex = -1)
    ld.ReadString(open("iris.txt","r").read(), True)
    
    nb = NaiveBayes(ld)
    nb.NaiveBayes()
    print "1", nb.Classify2([5.1,3.7,1.5,0.4])
    print "-1", nb.Classify2([6.3,2.5,4.9,1.5])

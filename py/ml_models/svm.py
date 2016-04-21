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

from sklearn import metrics
from sklearn.svm import SVC

class SVM(ModelBase):
    def __init__(self, dataset, *args, **kwargs):
        '''
            dataset: (datasets.localdata) 
            classfeatureindex: index of the column which defines the feature in dataset 
        '''
        ModelBase.__init__(self, dataset, 'SVM', *args, **kwargs)
        self.Test = self.Classify
        self.Apply = self.ClassifyDataset
        self.Train = self.NaiveBayes
        self.Save = self.Dump
        self.Load = self.LoadFromFile
        self.Graph = self.ShowImage
        # use default
        # self.T = self.RealValue
        self.model = GaussianNB()

    def NaiveBayes(self):
        pass


    def Classify(self, test):
        '''
            predict a single new sample input with trained tree
        '''

    def ClassifyDataset(self, dataset, remove_item = None):
        '''
            predict a series sample inputs from a dataset
        '''
    def Dump(self, filename):
        fw = open(filename, 'w')
        pickle.dump(self.model)
        fw.close()

    def LoadFromFile(self, filename):
        fr = open(filename)
        self.tree = pickle.load(self.model)

    def ShowImage(self, op):
        # tr = GraphTree()
        # # JSON can't have non-string key
        # tr.load(self.tree)
        # return tr.createPlot(show = False)

    def RealValue(self, op):
        pass
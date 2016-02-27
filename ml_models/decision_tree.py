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
from graphic.tree import *

class DecisionTree(ModelBase):
    def __init__(self, dataset, *args, **kwargs):
        '''
            dataset: (datasets.localdata) 
            classfeatureindex: index of the column which defines the feature in dataset 
        '''
        ModelBase.__init__(self, dataset, 'DECISION_TREE', *args, **kwargs)
        self.Test = self.Classify
        self.Apply = self.ClassifyDataset
        self.Train = self.BuildTree
        self.Save = self.DumpTree
        self.Load = self.LoadTree
        self.Graph = self.ShowImage
        # use default
        # self.T = self.RealValue
        self.tree = {}

    #这两个函数相对"独立"
    def ShannonEntropy(self, dataset = None):
        if dataset == None:
            dataset = self.dataset
        feature_count = ReduceByKeyAsDict(dataset.Iter(), dataset.classfeatureindex, \
            lambda (key,value):(key,len(value)), True, returnDataset = True)
        shentr = reduce(lambda x,y:x-y*math.log(y,2), map(lambda (key,value): \
            float(value)/self.dataset.Length(),feature_count.iteritems()),0)
        return shentr

    def SplitDataset(self, dataset, classfeatureindex):
        '''
            e.g. feature A is the best split feature and it has value True and False (represented by classfeaturevalue)
            Use classfeatureindex to split dataset
            Return:
            feature_value:[datasets_divided_by_this_feature]
            shentr:
        '''
        featurevalues = GroupByKey(dataset.Iter(), classfeatureindex, True)
        shentr = reduce(operator.add, map(lambda (key,value): \
            len(value)/float(self.dataset.Length())*self.ShannonEntropy(L2DS(value)),featurevalues.iteritems()),0)
        return featurevalues, shentr

    def BestFeature(self, dataset):
        '''
            return the feature best split the dataset INTEGER
        '''
        origin_entropy = self.ShannonEntropy()
        best_gain = 0.0 #g is infomation gain
        best_featureid = 0 
        # DO NOT INCLUDE CLASSFEATUREINDEX
        for i in xrange(dataset.ColumnLength()):
            if dataset.RealIndex(i) == dataset.RealIndex(dataset.classfeatureindex):
                continue
            feature, new_entropy = self.SplitDataset(dataset, i)
            infomation_gain = new_entropy - origin_entropy
            if infomation_gain > best_gain:
                best_gain = infomation_gain
                best_featureid = i
        return best_featureid

    def MajorityCount(self, classfeatures):
        '''
            TEST: USE DATA LIKE:
            yes;no;no;no;(only one class column)
            get the major value of one feature
            e.g feature A has values 1,1,1,1,0,0 in 6 items
            MajorityCount return 1
        '''
        return sorted(Counts(classfeatures).iteritems(), key = operator.itemgetter(1), reverse = True)[0][0]

    def CreateTree(self, dataset):
        '''
            build recursive decision tree
            dataset part of self.dataset
            classfeatures is a list of class-feature values in each item
        '''
        classfeatures = dataset.Column(dataset.classfeatureindex)
        if len(classfeatures) == 0:
            #empty dataset
            return None
        elif classfeatures.count(classfeatures[0]) == len(classfeatures):
            #all items share same class
            return classfeatures[0]
        if dataset.ColumnLength() == 1:
            #if only one feature left, choose which value of this feature is in major
            return self.MajorityCount(classfeatures)
        bestfeature = self.BestFeature(dataset)
        mytree = {dataset.head[bestfeature]:{}}
        featurevalues, shentr = self.SplitDataset(dataset, bestfeature)
        for value in featurevalues.keys():
            newdataset = dataset.Spawn(range(0,bestfeature)+range(bestfeature+1,dataset.ColumnLength()), items = featurevalues[value])
            mytree[dataset.head[bestfeature]][value] = self.CreateTree(newdataset)
        return mytree

    def BuildTree(self):
        self.tree = self.CreateTree(self.dataset)
        return self.tree

    def Classify(self, test):
        '''
            predict a single new sample input with trained tree
        '''
        tree = self.tree
        while True:
            featureindex = tree.keys()[0]
            branch_dict = tree[featureindex]
            for key in branch_dict.keys():
                if test[self.dataset.head.index(featureindex)] == key:
                    if type(branch_dict[key]).__name__ == 'dict':
                        tree = branch_dict[key]
                        break #jump out of for-loop, compare the next feature
                    else:
                        return branch_dict[key]

    def ClassifyDataset(self, dataset, remove_item = None):
        '''
            predict a series sample inputs from a dataset
        '''
        resultdataset = LocalData(None, head = self.dataset.head+['result'], classfeatureindex = -1)
        for item in dataset.Iter():
            resultdataset.items.append(item+[self.Classify(item)])
        return resultdataset

    def DumpTree(self, filename):
        fw = open(filename, 'w')
        pickle.dump(self.tree, fw)
        fw.close()

    def LoadTree(self, filename):
        fr = open(filename)
        self.tree = pickle.load(fr)

    def ShowImage(self, op):
        tr = GraphTree()
        # JSON can't have non-string key
        tr.load(self.tree)
        return tr.createPlot(show = False)

    def RealValue(self, op):
        pass

if __name__ == '__main__':
    def my_mapper(data, colindex, head):
        # return {
        #   'water': int(data),
        #   'foot': int(data),
        #   'fish': str(data)
        # }[head]
        if head == 'water':
            return int(data)
        elif head == 'foot':
            return int(data)
        else:
            return str(data)
    ld = datasets.localdata.LocalData(datamapper=my_mapper)
    ld.ReadString(open("dat_cls.txt","r").read(),True)
    dt = DecisionTree(ld)
    # for x in dt.dataset.items:
    #     print x, type(x)
    # print dt.dataset
    # print [item for item in dt.dataset.items]
    dt.BuildTree()
    print dt.tree

    
    print dt.Classify([1,1])
    print dt.Classify([0,0])
    dt.ShowImage('')
    # print dt.BestFeature(dt.dataset.items)

#coding:utf8
import sys
sys.path.append('..')

import math
import datasets
from datasets.localdata import *
from datasets.monads import *
import operator
import json
import pickle

class DecisionTree:
    def __init__(self, dataset, classfeatureindex = -1):
        '''
            dataset: (datasets.localdata) 
            classfeatureindex: index of the column which defines the feature in dataset 
        '''
        self.dataset = dataset
        self.classfeatureindex = classfeatureindex
        self.tree = {}
    def ShannonEntropy(self, items = None):
        if items == None:
            items = self.dataset.items
        feature_count = ReduceByKeyAsDict(items, self.classfeatureindex, lambda (key,value):(key,len(value)), True)
        shentr = reduce(lambda x,y:x-y*math.log(y,2), map(lambda (key,value):float(value)/len(items),feature_count.iteritems()),0)
        return shentr
    def SplitDataset(self, items, classfeatureindex):
        '''
            e.g. feature A is the best split feature and it has value True and False (represented by classfeaturevalue)
            Use classfeatureindex to split dataset
            Return:
            {feature_value:[datasets_divided_by_this_feature]}
        '''
        featurevalues = GroupByKey(items, classfeatureindex, True)
        shentr = reduce(operator.add, map(lambda (key,value):len(value)/float(len(items))*self.ShannonEntropy(value),featurevalues.iteritems()),0)
        return featurevalues, shentr
    def BestFeature(self, datasetitems):
        '''
            return the feature best split the dataset
            Usage:
            self.BestFeature(self.dataset.items)
        '''
        origin_entropy = self.ShannonEntropy()
        best_gain = 0.0 #g is infomation gain
        best_featureid = 0
        for i in xrange(len(datasetitems[0])):
            feature, new_entropy = self.SplitDataset(datasetitems, i)
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
    def CreateTree(self, datasetitems, headindex):
        '''
            build recursive decision tree
            datasetitems part of self.dataset.items
            headindex range(len(self.dataset.head)) avoid charset problems
            classfeatures is a list of class-feature values in each item
        '''
        classfeatures = [item[self.classfeatureindex] for item in datasetitems]
        if len(classfeatures) == 0:
            #empty dataset
            return None
        elif classfeatures.count(classfeatures[0]) == len(classfeatures):
            #all items share same class
            return classfeatures[0]
        if len(datasetitems[0]) == 1:
            #if only left classfeature column, choose which value of this feature is in major
            return self.MajorityCount(classfeatures)
        bestfeature = self.BestFeature(datasetitems)
        mytree = {headindex[bestfeature]:{}}
        featurevalues, shentr = self.SplitDataset(datasetitems, bestfeature)
        for value in featurevalues.keys():
            mytree[headindex[bestfeature]][value] = self.CreateTree(featurevalues[value], headindex[:bestfeature]+headindex[bestfeature+1:])
        return mytree
    def BuildTree(self):
        self.tree = self.CreateTree(self.dataset.items, range(len(self.dataset.head)))
        return self.tree
    def Classify(self, test):
        '''
            predict new samples with trained tree
        '''
        tree = self.tree
        while True:
            featureindex = tree.keys()[0]
            branch_dict = tree[featureindex]
            for key in branch_dict.keys():
                if test[featureindex] == key:
                    if type(branch_dict[key]).__name__ == 'dict':
                        tree = branch_dict[key]
                        break #jump out of for-loop, compare the next feature
                    else:
                        return branch_dict[key]

    def DumpTree(self, filename):
        fw = open(filename, 'w')
        pickle.dump(self.tree, fw)
        fw.close()
    def LoadTree(self, filename):
        fr = open(filename)
        return pickle.load(filename)
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
    dt = DecisionTree(ld,-1)
    print dt.BuildTree()
    # print dt.Classify([1,1])
    # print dt.Classify([0,0])
    # print dt.BestFeature(dt.dataset.items)

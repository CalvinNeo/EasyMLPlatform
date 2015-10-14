#coding:utf8
import sys
sys.path.append('..')

import math
import datasets.localdata
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
        feature_count = {}
        if items == None:
            items = self.dataset.items
        for item in items:
            current_feature = item[self.classfeatureindex]
            if current_feature not in feature_count.keys():
                feature_count[current_feature] = 1
            else:
                feature_count[current_feature] += 1
        shentr = 0.0
        for key in feature_count:
            p = float(feature_count[key]) / len(items)
            shentr -= p * math.log(p, 2)
        return shentr
    def SplitDataset(self, datasetitems, classfeatureindex):
        '''
            e.g. feature A is the best split feature and it has value True and False (represented by classfeaturevalue)
            Use classfeatureindex to split dataset
            Return:
            {feature_value:[datasets_divided_by_this_feature]}
        '''
        featurevalues = {} #
        for item in datasetitems:
            feature_value = item[classfeatureindex]
            if feature_value not in featurevalues.keys():
                featurevalues[feature_value] = []
            #这里必须要有0:和:-1,考虑到classfeatureindex=-1时,classfeatureindex+1=0
            newitem = item[:]
            del newitem[classfeatureindex]
            featurevalues[feature_value].append(newitem)
            # featurevalues[feature_value].append(item[0:classfeatureindex]+item[classfeatureindex+1:])
        shentr = 0.0
        for feature in featurevalues.keys():
            conditional_entropy = len(featurevalues[feature]) / float(len(datasetitems)) * self.ShannonEntropy(featurevalues[feature])
            shentr += conditional_entropy
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
            get the major value of one feature
            e.g feature A has values 1,1,1,1,0,0 in 6 items
            MajorityCount return 1
        '''
        classcount = {}
        for vote in classfeatures:
            if vote not in classcount.keys():
                classcount[vote] = 0
            classcount[vote] += 1
        sortedclasscount = sorted(classcount.iteritems(), key = operator.itemgetter(1), reverse = True)
        return sortedclasscount[0][0]
    def CreateTree(self, datasetitems, headindex):
        '''
            build recursive decision tree
            datasetitems self.dataset.items
            headindex range(len(self.dataset.head)) avoid charset problems
        '''
        classfeatures = [item[self.classfeatureindex] for item in datasetitems]
        if len(classfeatures) == 0:
            #empty dataset
            return None
        elif classfeatures.count(classfeatures[0]) == len(classfeatures):
            #all items share same class
            return classfeatures[0]
        if len(datasetitems[0]) == 1:
            #if only one feature left, choose which value of this feature is in major
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
    print dt.Classify([1,1])
    # print dt.BestFeature(dt.dataset.items)

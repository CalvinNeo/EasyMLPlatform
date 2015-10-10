#coding:utf8
import sys
sys.path.append('..')

import math
import datasets.localdata
import operator

class DecisionTree:
    def __init__(self, dataset, classfeatureindex = -1):
        self.dataset = dataset
        self.classfeatureindex = classfeatureindex #index of the column which defines the feature in dataset
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
            Use classfeatureindex to split dataset
            Return:
            {feature_value:[datasets_divided_by_this_feature]}
        '''
        featurevalues = {} #
        for item in datasetitems:
            feature_value = item[classfeatureindex]
            if feature_value not in featurevalues.keys():
                featurevalues[feature_value] = []
            featurevalues[feature_value].append(item[:classfeatureindex]+item[classfeatureindex+1:])
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
    def CreateTree(self, datasetitems, head):
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
        mytree = {head[bestfeature]:{}}
        featurevalues, shentr = self.SplitDataset(datasetitems, bestfeature)
        for value in featurevalues.keys():
            mytree[head[bestfeature]][value] = self.CreateTree(featurevalues[value], head[0:bestfeature]+head[bestfeature+1:])
        return mytree
        #e.g. feature A is the best split feature and it has value True and False (represented by classfeaturevalue)
        # classfeaturevalues = set([item[bestfeature] for item in dataset])
        # for value in classfeaturevalues
        #     self.SplitDataset()
        #     mytree[head[bestfeature]][value] = self.CreateTree(newdataset, head[0:bestfeature]+head[bestfeature+1:])
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
    ld = datasets.localdata.LocalData()
    ld.ReadString(open("dat_cls.txt","r").read(),True,mapper=my_mapper)
    dt = DecisionTree(ld,0)
    print dt.CreateTree(dt.dataset.items, dt.dataset.head)
    # print dt.BestFeature(dt.dataset.items)

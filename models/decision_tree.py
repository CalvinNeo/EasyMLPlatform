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
    def SplitDataset(self, classfeatureindex):
        '''
            Use classfeatureindex to split dataset
            Return:
            {feature_value:[datasets_divided_by_this_feature]}
        '''
        mainfeatures = {} #
        for item in self.dataset.items:
            current_feature = item[classfeatureindex]
            if current_feature not in mainfeatures.keys():
                mainfeatures[current_feature] = []
            mainfeatures[current_feature].append(item[:classfeatureindex]+item[classfeatureindex+1:])
        shentr = 0.0
        for feature in mainfeatures.keys():
            conditional_entropy = len(mainfeatures[feature]) / float(len(self.dataset.items)) * self.ShannonEntropy(mainfeatures[feature])
            shentr += conditional_entropy
        return feature, shentr
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
            feature, new_entropy = self.SplitDataset(i)
            infomation_gain = new_entropy - origin_entropy
            if infomation_gain > best_gain:
                best_gain = infomation_gain
                best_featureid = i
        return best_featureid
    def CreateTree(self, datasetitems):
        classfeatures = [item[self.classfeatureindex] for item in datasetitems]
        if len(classfeatures) == 0:
            #empty dataset
            return None
        elif classfeatures.count(classfeatures[0]) == len(classfeatures):
            #all items share same class
            return classfeatures[0]
        if len(datasetitems) == 1:
            pass
        bestfeature = self.BestFeature(datasetitems)

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
    print dt.BestFeature(dt.dataset.items)

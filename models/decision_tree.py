#coding:utf8
import sys
sys.path.append('..')

import math
import datasets.localdata

class DecisionTree:
    def __init__(self, dataset, featureindex = -1):
        self.dataset = dataset
        self.featureindex = featureindex #index of the column which defines the feature in dataset
    def ShannonEntropy(self, items = None):
        feature_count = {}
        if items == None:
            items = self.dataset.items
        for item in items:
            current_feature = item[self.featureindex]
            if current_feature not in feature_count.keys():
                feature_count[current_feature] = 1
            else:
                feature_count[current_feature] += 1
        shentr = 0.0
        for key in feature_count:
            p = float(feature_count[key]) / len(items)
            shentr -= p * math.log(p, 2)
        return shentr
    def SplitDataset(self, featureindex):
        mainfeatures = {} #{feature_value:[datasets_divided_by_this_feature]}
        for item in self.dataset.items:
            current_feature = item[featureindex]
            if current_feature not in mainfeatures.keys():
                mainfeatures[current_feature] = []
            mainfeatures[current_feature].append(item[:featureindex]+item[featureindex+1:])
        shentr = 0.0
        for feature in mainfeatures.keys():
            conditional_entropy = len(mainfeatures[feature]) / float(len(self.dataset.items)) * self.ShannonEntropy(mainfeatures[feature])
            shentr += conditional_entropy
        return feature, shentr
    def BestFeature(self):
        origin_entropy = self.ShannonEntropy()
        best_gain = 0.0 #g is infomation gain
        best_featureid = 0
        for i in xrange(len(self.dataset.items[0])):
            feature, new_entropy = self.SplitDataset(i)
            infomation_gain = new_entropy - origin_entropy
            if infomation_gain > best_gain:
                best_gain = infomation_gain
                best_featureid = i
        return best_featureid
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
    ld.readString(open("dat_cls.txt","r").read(),True,mapper=my_mapper)
    dt = DecisionTree(ld,0)
    print dt.BestFeature()

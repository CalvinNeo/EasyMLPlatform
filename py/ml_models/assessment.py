#coding:utf8
import sys
sys.path.append('..')

import datasets.localdata
import operator
import numpy as np
import sys
from collections import defaultdict, namedtuple
import datasets.localdata
from datasets.monads import *
from datasets.localdata import *
import itertools
from modelbase import ModelBase

       
class Assessment:
    def __init__(self, model, dataset):
        self.model = model
        self.dataset = dataset
        self.TP, self.TN, self.FP, self.FN = 0, 0, 0, 0
        self.Losses = [0.0] * self.dataset.Length()
        '''
            Protoclass in ['REGRESS', 'CLASSFY', 'CLUASTER']
        '''
        self.Protoclass = ModelBase.AllModelInfo()[self.model.prototype]['modeltype']

    def TFPN(self):
        '''
        Classify Judge
                            Positive    Negative
        Correct Prediction      TP         TN
        Wrong Prediction        FP         FN
        '''
        self.TP, self.TN, self.FP, self.FN = 0, 0, 0, 0
        for inp in self.dataset.Iter():
            a = self.model.Test(inp)
            t = self.model.T(inp)
            jugdepositive = lambda x: True if x >= (self.model.Positive + self.model.Negative) / 2 else False
            ja, jt = jugdepositive(a), jugdepositive(t)
            if ja == True and jt == True:
                self.TP += 1
            elif ja == True and jt == False:
                self.FP += 1
            elif ja == False and jt == True:
                self.FN += 1
            elif ja == False and jt == False:
                self.TN += 1
        if self.TP + self.FP == 0:
            self.P = 0
        else:
            self.P = self.TP / (self.TP + self.FP)
        if self.TP + self.FN == 0:
            self.R = 0
        else:
            self.R = self.TP / (self.TP + self.FN)
        if self.P == 0 or self.R == 0:
            self.F1 = 0
        else:
            self.F1 = 2.0 / (1.0 / self.P + 1.0 / self.R)

    def Loss(self):
        '''
        Regress Judge
        '''
        self.Losses, index = [0.0] * self.dataset.Length(), 0
        for inp in self.dataset.Iter():
            a = self.model.Test(inp)
            t = self.model.T(inp)
            loss = self.model.Loss(t, a)
            self.Losses[index] = loss
            index += 1

    def ROC(self):
        pass

    @staticmethod
    def SFoldValidate(s, train = False, models = []):
        '''
            s-fold cross validation
        '''
        if s > 1:
            if train:
                pass
            elif len(models) == s - 1:
                # Split dataset
                
                for md_index in xrange(len(models)):
                    models[md_index].Train()

        return None


if __name__ == '__main__':
    # i = 5
    # while i > 1:
    #     print i
    #     i-=1
    # else:
    #     print "haha"
    # print '-------------'
    # while False:
    #     print "False"
    # else:
    #     print True
    print type(np.array([1,2])).__name__
    print type(np.matrix('1 2')).__name__
    print 1 in [1,2,3]
    print np.sum(np.vectorize(lambda n:0 if n==0.0 else 1)([0,1,2,3]))
    print "------------"
    print EuclideanDist([1,2],[3,4])
#coding:utf8
import sys
sys.path.append('..')

import math
import datasets.localdata
import operator
import numpy as np
import sys
from collections import defaultdict, namedtuple
import itertools

def L0(vec):
    '''
        count of non-zero elements of a vector
    '''
    if type(vec).__name__ in ['matrix','ndarray']:
        return np.sum(np.vectorize(lambda n:0 if n==0.0 else 1)(vec))
    else:
        return np.sum(np.vectorize(lambda n:0 if n==0.0 else 1)(np.matrix(vec)))

def L1(vec):
    '''
        sum(abs(for each elements in a vector))
    '''
    if type(vec).__name__ in ['matrix','ndarray']:
        return np.sum(np.vectorize(lambda n:abs(n))(vec))
    else:
        return np.sum(np.vectorize(lambda n:abs(n))(np.matrix(vec)))

def L2(vec):
    '''
        sqrt(sigma(square each elements))
    '''
    if type(vec).__name__ in ['matrix','ndarray']:
        return np.sum(np.vectorize(lambda n:n**2)(vec))**0.5
    else:
        return np.sum(np.vectorize(lambda n:n**2)(np.matrix(vec)))**0.5

def EuclideanDist(vec1, vec2):
    '''
        Euclidean Distance:
            sqrt(sigma((vec1[i] - vec2[i]) ^ 2))
    '''
    if type(vec1).__name__ in ['matrix','ndarray']:
        r = vec1-vec2
        return np.trace(np.dot(r,r.T))**0.5
    else:
        r = np.matrix(vec1) - np.matrix(vec2)
        return np.trace(np.dot(r,r.T))**0.5

def ManhattanDist(vec1, vec2):
    '''
        ManhattanDist Distance:
            sigma(abs(vec1[i] - vec2[i]))
    '''
    if type(vec1).__name__ in ['matrix','ndarray']:
        pass
    else:
        pass
        
class Assessment:
    def __init__(self, model, dataset, inputs):
        self.model = model
        self.dataset = dataset
        self.inputs = inp
        self.TP, self.TN, self.FP, self.FN = 0, 0, 0, 0

    def TFPN(self):
        '''
        Classify Judge
                            Positive    Negative
        Correct Prediction      TP         TN
        Wrong Prediction        FP         FN
        '''
        for inp in self.inputs:
            a = self.model.Test(inp)

    def MeanSquare(self):
        '''
        Regress Judge
        '''

    def P(self):
        return self.TP / (self.TP + self.FP)

    def R(self):
        return self.TP / (self.TP + self.FN)

    def F1(self):
        return 2.0 / (1.0 / self.P() + 1.0 / self.R())

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
                pass

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
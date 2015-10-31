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
        pass
    else:
        pass

def L1(vec):
    '''
        sum(abs(for each elements in a vector))
    '''
    if type(vec).__name__ in ['matrix','ndarray']:
        pass
    else:
        pass

def L2(vec):
    '''
        sqrt(sigma(square each elements))
    '''
    if type(vec).__name__ in ['matrix','ndarray']:
        pass
    else:
        pass

def EuclideanDist(vec1, vec2):
    '''
        Euclidean Distance:
            sqrt(sigma((vec1[i] - vec2[i]) ^ 2))
    '''
    if type(vec).__name__ in ['matrix','ndarray']:
        pass
    else:
        pass
def ManhattanDist(vec1, vec2):
    '''
        ManhattanDist Distance:
            sigma(abs(vec1[i] - vec2[i]))
    '''
    if type(vec).__name__ in ['matrix','ndarray']:
        pass
    else:
        pass

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
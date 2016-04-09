#coding:utf8
import sys
sys.path.append('..')

import csv
from optparse import OptionParser
import operator
from localdata import *
import localdata
import ast

'''
    dataset.items is deprecated
    dataset.Iter() recommended
'''
def L2DS(lst, head=None, classfeatureindex=-1):
    '''
        input list output Dataset
    '''
    ld = localdata.LocalData(datamapper=None, head=head, items=lst, classfeatureindex=classfeatureindex)
    return ld

def D2DS(dct):
    '''
        input dict output Dataset
    '''
    return dct

def lmdaprint(text):
    print "lamdaprint: ", text
    
def ReduceByKeyAsList(items, keyindex, lmda, lmdamap=None, removekey=False, returnDataset=False):
    g = GroupByKey(items, keyindex, removekey)
    '''
        recieve a list
        map(lambda key: ... , g) --value(maybe a list) to each key
        map(lmdamap, g[key]) --reduce for each in value
        return a list or dataset according to returnDataset
        In:
        1,1,2
        1,2,3
        2,2,2
        4,7,9
        Out(reduce by lambda x,y:x + y where keyindex = 0):
        [[1, 1, 2, 1, 2, 3], [2, 2, 2], [4, 7, 9]] ---> join 
        Out(reduce by lambda x,y:x + y where keyindex = 0, lmdamap = len(x)): ---> get sum of len
        [6, 3, 3]
    '''
    r = map(lambda key:reduce(lmda, map(lmdamap, g[key])), g)
    return L2DS(r) if returnDataset else r

def ReduceByKeyAsDict(items, keyindex, lmdakeyvalue, removekey=False, returnDataset=False):
    g = GroupByKey(items, keyindex, removekey)
    '''
        recieve a list
        lmdakeyvalue get a (key, value) tuple, return a tuple (f(key), g(value)), f,g are some given functions
        return a dict
    '''
    r = dict(map(lmdakeyvalue, g.iteritems()))
    return D2DS(r) if returnDataset else r

def GroupByKey(items, keyindex, removekey=False, returnDataset=False):
    '''
        recieve a list
        return a dict

        split dataset into a dictionary classified by keys, if keyindex = None EQUALS Group


        In:
        a,1,3
        a,2,3
        b,1,1
        c,3,3
        d,3,4
        keyindex == 0(the colomn of [a,a,b,c,d])

        Out:
        (if removekey)
        {a:[1,2,3,3], b:[1,1],c:[3,3,3,4]}
        (if not removekey)
        {a:[a,1,2,3,3], b:[b,1,1],c:[c,3,3,3,4]}
    '''
    groups = {}
    for item in items:
        value = item[keyindex]
        if value not in groups.keys():
            if removekey:
                groups[value] = [item[0:keyindex] + item[keyindex+1:] if keyindex > -1 else item[:len(item)-1]]
            else:
                groups[value] = [item]
        else:
            if removekey:
                groups[value].append(item[0:keyindex] + item[keyindex+1:] if keyindex > -1 else item[:len(item)-1])
            else:
                groups[value].append(item)
    return L2DS(groups) if returnDataset else groups

def SortByKey(items, keyindex, comparelmda, removekey=False, returnDataset=False):
    '''
        recieve a list
        Group the list by Key(call GroupByKey)
        Sort According to Key
    '''
    g = GroupByKey(items, keyindex, removekey)
    r = sorted(g, cmp=comparelmda)
    return D2DS(r) if returnDataset else r

def Count(items, lmda):
    '''
        recieve a list
        Assertion:
        lmda must be True/False lambda function, return True if such condition should be counted, False otherwise
    '''
    return reduce(operator.add, map(lambda x:1 if lmda(x)==True else 0, items))
    
def Counts(items):
    '''
        e.g.
        in: 1,1,2,2,2,4
        out: {1:2, 2:3, 4:1}
    '''
    groups = {}
    for item in items:
        if item not in groups.keys():
            groups[item] = 1
        else:
            groups[item] += 1
    return groups
if __name__ == '__main__':
    ld = LocalData(datamapper = lambda data,colindex,head:int(data))
    ld.ReadString(open("1.txt","r").read(),True)
    print GroupByKey(ld.items, 0)
    print GroupByKey(ld.items, 0,True)
    print ReduceByKeyAsList(ld.Iter(), 0, lambda x,y:x + y,lambda x:len(x),removekey=False, returnDataset=False)
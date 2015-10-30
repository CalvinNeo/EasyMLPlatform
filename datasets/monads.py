#coding:utf8
import sys
sys.path.append('..')

import csv
from optparse import OptionParser
import operator
from localdata import *

def ReduceByKeyAsList(items, keyindex, lmda, removekey=False):
    g = GroupByKey(items, keyindex, removekey)
    '''
        map(lambda key:g[key], g) --value(maybe a list) to each key
        map(lambda key:g[key], g) --reduce for each in value
        return a list
    '''
    return map(lambda key:reduce(lmda, g[key]), g)
def ReduceByKeyAsDict(items, keyindex, lmdakeyvalue, removekey=False):
    g = GroupByKey(items, keyindex, removekey)
    '''
        lmdakeyvalue get a (key, value) tuple, return a tuple (f(key),g(value)), f,g are some defined functions
        return a dict
    '''
    return dict(map(lmdakeyvalue, g.iteritems()))
def GroupByKey(items, keyindex, removekey=False):
    '''
        split dataset into a dictionary classified by keys
        if keyindex = None EQUALS Group
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
    return groups
def SortByKey(items, keyindex, comparelmda, removekey=False):
    g = GroupByKey(items, keyindex, removekey)
    return sorted(g, cmp=comparelmda)
def Count(items, lmda):
    '''
        Assertion:
        lmda must be True/False lambda function, return True if such condition should be counted, False otherwise
    '''
    return reduce(operator.add, map(lambda x:1 if lmda(x)==True else 0, items))
def Counts(items):
    '''
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

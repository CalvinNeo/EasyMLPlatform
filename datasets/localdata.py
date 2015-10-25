#coding:utf8
import sys
sys.path.append('..')

import csv
from optparse import OptionParser
import operator

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

class LocalData:
    def __init__(self, datamapper):
        self.head = []
        self.items = []
        self.datamapper = datamapper
    def ReadString(self, data, hasHead = False, attr_delim = ",", record_delim = "\n", getValue=True):
        '''
            generate head 1,2,3... if there are no heads
        '''
        records = data.split(record_delim)
        if hasHead:
            self.head = records[0].split(attr_delim)
            del records[0]
        else:
            self.head = []
        self.items = []
        '''
            Usage:
            def my_mapper(data, colindex, head):
                return {
                  'water': int(data),
                  'foot': int(data),
                  'fish': str(data)
                }[head]
        '''
        if getValue:
            for record in records:
                if record == "":
                    break
                data_col = record.split(attr_delim)
                #(value,column,head)
                if not hasHead: #if no head set head as 0,1,2,3,4,5,6...
                    self.head = range(len(data_col))
                    hasHead = True
                self.items.append(map(self.datamapper,data_col,range(len(data_col)),self.head))
    def ReadCSV(self, path, hasHead):
        pass
    def ReadXML(self, path, hasHead):
        pass
    def ReadXLS(self, path, hasHead):
        pass
    def ReadTXT(self, path, hasHead):
        pass

    def SaveCSV(self, path, saveHead = True):
        with open(path, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            if saveHead:
                spamwriter.writerow(self.head)
            for x in self.items:
                spamwriter.writerow(x)
if __name__ == '__main__':
    ld = LocalData(datamapper = lambda data,colindex,head:int(data))
    ld.ReadString(open("1.txt","r").read(),True)
    ld.SaveCSV("k.csv")
    print ld.head
    print ld.items
    print GroupByKey(ld.items, 0)
    print GroupByKey(ld.items, 0,True)
    print Count(ld.items, lambda x:x[0]==1)    
    print ReduceByKeyAsList(ld.items, 0, lambda x,y:x+y) #join list



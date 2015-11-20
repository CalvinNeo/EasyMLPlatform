#coding:utf8
import sys
sys.path.append('..')

import csv
from optparse import OptionParser
import operator
from monads import *
import crawl

class LocalData:
    def __init__(self, datamapper, *args, **kwargs):
        if 'head' in kwargs.keys() and kwargs['head'] != None:
            self.head = kwargs['head']
        else:
            self.head = []
        if 'items' in kwargs.keys() and kwargs['items'] != None:
            self.items = kwargs['items']
        else:
            self.items = []
        if 'online' in kwargs.keys() and kwargs['online'] != None:
            self.online = kwargs['online']
        else:
            self.online = False
        '''
            classfeatureindex is the index of the column which defines the feature in dataset 
            (if the dataset is used to classify or regress)
        '''
        if 'classfeatureindex' in kwargs.keys():
            self.classfeatureindex = kwargs['classfeatureindex']
        else:
            self.classfeatureindex = -1
        '''
            mode:
            all -all items in dataset will be used to train
            sfold -sfold cross validation

        '''        
        self.mode = 'all'
        '''
            Usage:
            def my_mapper(data, colindex, head):
                return {
                  'water': int(data),
                  'foot': int(data),
                  'fish': str(data)
                }[head]
            datamapper is parse raw data
        '''
        self.datamapper = datamapper
    def __str__(self):
        return "DATASET: " + str(self.head) + " " + str(self.items) + " " + str(self.classfeatureindex)

    def Iter(self):
        if self.online:
            pass
        else:
            if self.mode == 'all':
                for item in self.items:
                    yield item
    def Item(self, i):        
        if self.online:
            pass
        else:
            if self.mode == 'all':
                return self.items[i]
    def Length(self):               
        if self.online:
            pass
        else:
            if self.mode == 'all':
                return len(self.items)
    def ColumnLength(self):          
        if self.online:
            pass
        else:
            if self.mode == 'all':
                return len(self.head)
    def Column(self, i):          
        if self.online:
            pass
        else:
            if self.mode == 'all':
                return [item[i] for item in self.items]
    def Spawn(self, colindexs, *args, **kwargs):
        newhead = [self.head[i] for i in colindexs]
        if 'items' in kwargs.keys() and kwargs['items'] != None:
            newitems = list(kwargs['items'])
        else:
            newitems = [[self.items[i][j] for j in colindexs] for i in kwargs['linindexs']]
        print "classfeatureindex", self.classfeatureindex, colindexs
        positiveindex = self.ColumnLength() + self.classfeatureindex if self.classfeatureindex < 0 else self.classfeatureindex
        newclassfeatureindex = colindexs.index(positiveindex) if positiveindex in colindexs else -1
        return LocalData(self.datamapper, head = newhead, items = newitems, classfeatureindex = newclassfeatureindex)
    def SpawnRect(self, x1, y1, x2, y2, cpy=True):
        pass
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
    def ReadCSV(self, path, hasHead=False, getValue=True):
        self.ReadString(open(path, 'r'), hasHead, getValue)
    def ReadXML(self, path, hasHead=False, getValue=True):
        pass
    def ReadXLS(self, path, hasHead=False, getValue=True):
        pass
    def ReadTXT(self, path, hasHead=False, getValue=True):
        self.ReadString(open(path, 'r'), hasHead, getValue)

    def SaveCSV(self, path, saveHead = True):
        with open(path, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            if saveHead:
                spamwriter.writerow(self.head)
            for x in self.items:
                spamwriter.writerow(x)

    def SetURL(self, urls, search_lmda = None, iter_lmda = None, *args, **kwargs):
        if type(urls.__name__) != 'list':
            urls = [urls]

class TestClass:
    def __init__(self):
        self.d = [1,2,3,4,5,6]
        self.mode = 'haha'
    def Iter(self):
        if self.mode == 'haha':
            for i in self.d:
                yield i
        else:
            for i in self.d:
                yield 'i'
if __name__ == '__main__':
    ld = LocalData(datamapper = lambda data,colindex,head:int(data))
    ld.ReadString(open("1.txt","r").read(),True)
    ld.SaveCSV("k.csv")
    print ld.head
    for items in ld.Iter():
        print items
    print GroupByKey(ld.Iter(),0)
    print "----------------------"
    t = TestClass()
    j = 0
    for i in t.Iter():
        j += 1
        if j > 1:
            t.mode = 'nono'
        print i
    t.mode = 'nono'
    for i in t.Iter():
        print i
    print "-----------------"
    print ld.Spawn([0,1],linindexs = [0,1])
    print ld
    print "+++++++++++++++++++"
    print type([1,2,3]).__name__

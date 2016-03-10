#coding:utf8
import sys
sys.path.append('..')

import csv
from optparse import OptionParser
import operator
from monads import *
import crawl
import parse

class LocalData:
    def __init__(self, datamapper = None, *args, **kwargs):
        '''
            head
            items
            online
            classfeatureindex
            mode
            dstype
            datamapper
            crawl
        '''
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
            dstype is the type of dataset include:
            table
            JSON
        '''
        if 'dstype' in kwargs.keys():
            self.dstype = kwargs['dstype']
        else:
            self.dstype = 'table'       
        '''
            Usage:
            def my_mapper(data, colindex, head):
                return {
                  'water': int(data),
                  'foot': int(data),
                  'fish': str(data)
                }[head]
            or 
            datamapper = lambda data,colindex,head:int(data)

            datamapper read raw data from str to other types you want
            datamapper DO NOT parse raw data
            FOR MOST TIMES
            use `parse` module is enough
        '''
        if datamapper == None:
            self.datamapper = self.default_datamapper
        else:
            self.datamapper = datamapper

        self.crawl = None

    def __getitem__(self, i):
        return self.Item(i)

    def __len__(self):
        return self.Length()

    def __repr__(self):
        return  "{{ 'head':{}, 'items':{}, 'online':'{}' , 'classfeatureindex':{}, 'mode':'{}', 'dstype':'{}' }}" \
            .format( str(self.head), str(self.items), str(self.online), str(self.classfeatureindex), str(self.mode), 
                str(self.dstype))

    def __unicode__(self):
        return  "{{ 'head':{}, 'items':{}, 'online':'{}' , 'classfeatureindex':{}, 'mode':'{}', 'dstype':'{}' }}" \
            .format( str(self.head), str(self.items), str(self.online), str(self.classfeatureindex), str(self.mode), 
                str(self.dstype))

    def __str__(self):
        return  "{{ 'head':{}, 'items':{}, 'online':'{}' , 'classfeatureindex':{}, 'mode':'{}', 'dstype':'{}' }}" \
            .format( str(self.head), str(self.items), str(self.online), str(self.classfeatureindex), str(self.mode), 
                str(self.dstype))
            
    def default_datamapper(self, data, colindex, head):
        return parse.parsestr(data, [parse.extendboolean])

    # def GenerateHead(self, ncol):
    #     self.head = range(len(ncol))

    def Iter(self):
        if self.online:
            self.OnlineRenew()

        if self.mode == 'all':
            for item in self.items:
                yield item
        elif self.mode == 'sfold':
            for index in xrange(0, len(self.items), self.nsplit):
                yield self.items[index]

    def Item(self, i):
        if self.online:
            self.OnlineRenew()

        if self.mode == 'all':
            return self.items[i]
        elif self.mode == 'sfold':
            return self.items[i*self.nsplit]

    def Length(self):
        if self.online:
            self.OnlineRenew()

        if self.mode == 'all':
            return len(self.items)
        elif self.mode == 'sfold':
            return int(len(self.items) / self.nsplit)

    def ColumnLength(self):
        if self.online:
            self.OnlineRenew()

        if self.mode == 'all':
            return len(self.head)
        elif self.mode == 'sfold':
            return int(len(self.head) / self.nsplit)

    def Column(self, i):
        if self.online:
            self.OnlineRenew()

        if self.mode == 'all':
            return [item[i] for item in self.items]
        elif self.mode == 'sfold':
            return [self.items[index][i] for index in xrange(0, len(self.items), self.nsplit)] 

    def HeadIndex(self, i, head_col):
        '''
            get head index(in col start from 0) from head name(string)
        '''
        if self.online:
            self.OnlineRenew()

        if self.mode == 'all':
            return self.items[i][self.head.index(head_col)]
        elif self.mode == 'sfold':
            return [self.items[index][i] for index in xrange(0, len(self.items), self.nsplit)] 

    def RealIndex(self, index):
        '''
            in: -1
            out: len(self.head) - 1
        '''
        return self.ColumnLength() + index if index < 0 else index

    def Spawn(self, colindexs, *args, **kwargs):
        newhead = [self.head[i] for i in colindexs]
        if 'items' in kwargs.keys() and kwargs['items'] != None:
            newitems = list(kwargs['items'])
        else:
            newitems = [[self.items[i][j] for j in colindexs] for i in kwargs['linindexs']]
        # print "classfeatureindex", self.classfeatureindex, colindexs
        positiveindex = self.RealIndex(self.classfeatureindex)
        newclassfeatureindex = colindexs.index(positiveindex) if positiveindex in colindexs else -1
        return LocalData(self.datamapper, head = newhead, items = newitems, classfeatureindex = newclassfeatureindex)
    
    def SpawnRect(self, col1, col2, row1, row2, cpy=True):
        '''
            head
            items
            online
            classfeatureindex
            mode
            dstype
            datamapper
            crawl
        '''

    def Trim(self, col1, col2, row1, row2):
        if self.mode == 'all':
            self.items = self.items[x1:x2]
        elif self.mode == 'sfold':
            for index in xrange(0, len(self.items), self.nsplit):
                yield self.items[index]

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
                # self.items.append(map(self.datamapper, data_col, range(len(data_col)), self.head))
                # self.items.append( self.datamapper( data_col, range(len(data_col)), self.head ) )
                self.items.append(map(lambda x:self.datamapper(x[0],x[1],x[2]), zip(data_col, range(len(data_col)), self.head)))

    def ReadCSV(self, path, hasHead=False, getValue=True, attr_delim = ","):
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

    def SetURL(self, urls, locate, search_lmda = None, *args, **kwargs):
        if type(urls).__name__ != 'list':
            urls = [urls]
        if len(urls) > 0:
            self.crawl = crawl.Crawl(urls[0], locate, search_lmda, code='utf8')

    def OnlineRenew(self):
        if self.crawl != None:
            crawl_fetch = self.crawl.start()
            self.head, self.items = crawl_fetch['head'], crawl_fetch['items']
        for rec_id in xrange(len(self.items)):
            # (value,column,head)
            self.items[rec_id] = map(lambda x: self.datamapper(x[0],x[1],x[2]), zip(self.items[rec_id], range(len(self.items[rec_id])), self.head))

    def Encrypt(self, x):
        return x

    def DeCrypt(self):
        return x

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
    ld = LocalData()
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
    print range(0, 10, 3)
    print ld[0]

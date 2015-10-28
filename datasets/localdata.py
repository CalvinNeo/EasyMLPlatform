#coding:utf8
import sys
sys.path.append('..')

import csv
from optparse import OptionParser
import operator

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



#coding:utf8
import csv
from optparse import OptionParser
class LocalData:
    def __init__(self):
        self.head = []
        self.values = []
    def readString(self,data,hasHead = False,attr_delim = ",",record_delim = "\n",mapper = None,getValue=True):
        records = data.split(record_delim)
        if hasHead:
            self.head = records[0].split(attr_delim)
            del records[0]
        else:
            self.head = []
        self.values = []
        if getValue:
            for record in records:
                data_col = record.split(attr_delim)
                #(value,column,head)
                if not hasHead: #if no head set head as 0,1,2,3,4,5,6...
                    self.head = range(len(data_col))
                    hasHead = True
                self.values.append(map(mapper,zip(data_col,range(len(data_col)),self.head)))
    def readCSV(self,path,hasHead):
        pass
    def readXML(self,path,hasHead):
        pass
    def readXLS(self,path,hasHead):
        pass
    def readTXT(self,path):
        pass

    def saveCSV(self,path,saveHead = True):
        with open(path, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            if saveHead:
                spamwriter.writerow(self.head)
            for x in self.values:
                spamwriter.writerow(x)
if __name__ == '__main__':
    ld = LocalData()
    ld.readString(open("1.txt","r").read(),True,mapper=lambda x:int(x[0]))
    ld.saveCSV("k.csv")
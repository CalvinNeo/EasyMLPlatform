#coding:utf8
import csv
from optparse import OptionParser
def readString(data,hasHead = False,attr_delim = ",",record_delim = "\n",mapper = None,getValue=True):
	records = data.split(record_delim)
	if hasHead:
		head = records[0].split(attr_delim)
		del records[0]
	else:
		head = None
	values = []
	if getValue:
		for record in records:
			data_col = record.split(attr_delim)
			#(value,column)
			values.append(map(mapper,zip(data_col,range(len(data_col)))))
	return head,values
def readCSV(path,hasHead):
	pass
def readXML(path,hasHead):
	pass
def readXLS(path):
	pass

if __name__ == '__main__':
	print readString(open("1.txt","r").read(),True,mapper=lambda x:int(x[0]))
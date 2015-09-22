#coding:utf8
import csv
from optparse import OptionParser
def readString(data,hasHead = False,delim = ",",splitter = "\n",mapper = None):
	records = data.split(splitter)
	if hasHead:
		head = records[0].split(delim)
		del records[0]
	else:
		head = None
	values = []
	for record in records:
		values.append(map(mapper,record.split(delim)))
	return values,head
def readCSV(path,hasHead):
	pass
def readXML(path,hasHead):
	pass
def readXLS(path):
	pass

if __name__ == '__main__':
	print readString(open("1.txt","r").read(),True,mapper=lambda x:int(x))
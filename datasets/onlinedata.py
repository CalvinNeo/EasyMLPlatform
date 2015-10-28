#coding:utf8
import sys
sys.path.append('..')

import csv
from optparse import OptionParser
import operator

class OnlineData:
    def __init__(self, datamapper, head):
	    self.head = head
	    self.items = []
	    self.datamapper = datamapper
	def GrabItem(self):
		pass
	def ItemYield(self):
		'''
			return a yield of items
		'''
		pass
	def Collect(self):
		'''
			monitor and collect online dataset to string, TXT files etc;
		'''
		pass
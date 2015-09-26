#coding:utf8

import numpy as np
import math
import pylab as pl
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import json

class Tree:
	def __init__(self):
		self.jsonobj = {}
		self.leafNode = dict(boxstyle = 'round4',fc = '0.8')
		self.branchNode = dict(boxstyle = 'sawtooth',fc = '0.8')
		self.arrow = dict(arrowstyle = '<-')
		self.depth = 0
		self.leafcount = 0
	def get_depth_leafcount(self,root):
		current_node = root.keys()[0] #name of choice node(string)
		branch_dict = root[current_node]
		maxdepth, thisdepth, thisleafcount = 0,0,0
		for current_node in branch_dict.keys():
			print current_node,type(branch_dict[current_node]).__name__ 
			if type(branch_dict[current_node]).__name__ == 'dict':
				temp = self.get_depth_leafcount(branch_dict[current_node])
				thisdepth = 1 + temp[0]
				thisleafcount += temp[1]
			else:
				thisdepth = 1
				thisleafcount += 1
			if thisdepth > maxdepth:
				maxdepth = thisdepth
		return maxdepth,thisleafcount
	def load(self,strjson):
		self.jsonobj = dict(strjson)
		self.depth,self.leafcount = self.get_depth_leafcount(self.jsonobj)
	def plotMidText(self, cntrPt, parentPt, txtString):
		xMid = (parentPt[0]  - cntrPt[0]) / 2.0 + cntrPt[0]
		yMid = (parentPt[1]  - cntrPt[1]) / 2.0 + cntrPt[1]
		self.ax1.text(xMid, yMid, txtString)
	def plotNode(self, nodeTxt, cntrPt, parentPt, nodeType):
		self.ax1.annotate(nodeTxt, xy = parentPt, xycoords = 'axes fraction', xytext = cntrPt, \
			 textcoords = 'axes fraction', va = 'center', ha = 'center', bbox = nodeType, arrowprops = self.arrow)			
	def plotTree(self, myTree, parentPt, nodeTxt):
		depth, leaves = self.get_depth_leafcount(myTree)
		current_node = myTree.keys()[0]
		cntrPt = (self.xOff + (1.0 + leaves) / 2.0 / self.leafcount, self.yOff)
		self.plotMidText(cntrPt, parentPt, nodeTxt)
		self.plotNode(current_node, cntrPt, parentPt, self.branchNode)
		branch_dict = myTree[current_node]
		self.yOff -= 1.0 / self.depth	
		for current_node in branch_dict.keys():
			if type(branch_dict[current_node]).__name__ == 'dict':
				self.plotTree(branch_dict[current_node], cntrPt, str(current_node))
			else:
				self.xOff += 1.0 / self.leafcount
				self.plotNode(branch_dict[current_node], (self.xOff, self.yOff), cntrPt, self.leafNode)
				self.plotMidText((self.xOff, self.yOff), cntrPt, str(current_node))
		self.yOff += 1.0 / self.depth
	def createPlot(self):
		fig = plt.figure(1, facecolor = 'white')
		fig.clf()
		axprops = dict(xticks = [], yticks = [])
		self.ax1 = plt.subplot(111,frameon = False, **axprops)
		self.xOff, self.yOff = -0.5 / self.leafcount, 1.0
		self.plotTree(self.jsonobj, (0.5,1.0), '')
		plt.show()
if __name__ == '__main__':
	tr = Tree()
	# aa = '{"no surfacing":{"0":"no","1":{"flippers":{"0":"no","1":"yes"}}}}'
	# tr.load(json.loads(aa))
	aa = {"aged":{"0":"no","1":{"male":{"0":"no","1":"yes"}}}}
	print dict(aa)
	# aa = {"no surfacing":{0:"no",1:{"flippers":{0:"no",1:"yes"}}}}
	# print dict(aa)
	tr.load(aa)
	print tr.leafcount,tr.depth
	tr.createPlot()

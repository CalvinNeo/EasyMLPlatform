#coding:utf8
import sys
sys.path.append('..')

import numpy as np
import math
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import sys, glob, os
from collections import defaultdict, namedtuple
import itertools
import operator
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import datasets.localdata

class DataGraph:
    def __init__(self, dataset, classfeatureindex = -1, datamapper = None):
        self.dataset = dataset
        self.classfeatureindex = classfeatureindex #index of the column which defines the feature in dataset
        self.datamapper = datamapper
        self.JudgeScale()
        self.fig = plt.figure()
    def JudgeScale(self):
        '''
            determine lower/upper bound of X/Y coordinates
        '''
        if len(self.dataset.items) > 0:
            self.coorbound = [(0,0)] * len(self.dataset.items[0])
            for index in xrange(len(self.coorbound)):
                columns = [x[index] for x in self.dataset.items]
                self.coorbound[index] = (min(columns),max(columns))
    def DrawData(self, dimX, dimY = -1):
        ax = self.fig.add_subplot(111)
        xcord1 = []; ycord1 = []; xcord2 = []; ycord2 = []
        for item in self.dataset.items:
            print item,item[dimX],item[dimY]
            if item[dimY] > 0.5:
                xcord1.append(item[dimX]); ycord1.append(item[dimY])
            else:
                xcord2.append(item[dimX]); ycord2.append(item[dimY])
        ax.scatter(xcord1, ycord1, s = 30, c = 'red', marker = 's')
        ax.scatter(xcord2, ycord2, s = 30, c = 'green')
        plt.xlabel('X'); plt.ylabel('Y')
        plt.show()
if __name__ == '__main__':
    # dst_path = '../models'
    # ext_name = '*'
    # os.chdir( dst_path )
    # for f in glob.glob( ext_name ):
    #     print f
    def my_mapper(data, colindex, head):
        # return {
        #   'water': int(data),
        #   'foot': int(data),
        #   'fish': str(data)
        # }[head]
        if head == 'water':
            return int(data)
        elif head == 'foot':
            return int(data)
        else:
            if data == 'yes':
                return 1
            else:
                return 0
    ld = datasets.localdata.LocalData(datamapper=my_mapper)
    ld.ReadString(open("../models/dat_cls.txt","r").read(),True)
    dg = DataGraph(ld, -1)
    dg.DrawData(0,1)
    print "bound",dg.coorbound    
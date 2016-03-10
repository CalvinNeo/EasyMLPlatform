#coding:utf8
import numpy as np
import math
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D
import sys
from collections import defaultdict, namedtuple
import itertools
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def draw_contour(fun,dim1,dim2,tofilename):
	#DIM (scale_id,from,to,step)
	fig = pl.figure()
	X,Y = np.meshgrid(np.arange(dim1[0], dim1[1], dim1[2]),np.arange(dim2[0], dim2[1], dim2[2]))
	Z = np.vectorize(fun)(X,Y)
	pl.contourf(X,Y,Z)
	pl.colorbar()
	if tofilename != "":
		pl.savefig(tofilename)
	else:
		pl.show()
draw_contour(lambda x,y:math.sin(x+y),(-2,2,0.05),(-1,1,0.05),"D:/myfig")



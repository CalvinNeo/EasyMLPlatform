#coding:utf8

from numpy import *
import numpy

def gauss(a,b):
    n = len(b)
    for i in range(0,n-1):
        if a[i,i] == 0.0:
            for j in range(i+1,n):
                if a[i,j] != 0.0:
                    t = array(a[:,i]);a[:,i] = array(a[:,j]);a[:,j] = t
                    # t = array(b[i]);b[i] = array(b[j]);b[j] = t
        for j in range(i+1,n):
            if a[j,i] != 0.0:
                lam = float(a[j,i])/a[i,i]
                a[j,(i+1):n] -= lam*a[i,(i+1):n]
                b[j] -= lam*b[i]
    for i in range(n-1,-1,-1):
        b[i] = (b[i] - dot(a[i,(i+1):n],b[(i+1):n]) ) / a[i,i]
    result = b
    return result

x = matrix([[2.0,2.0,-1.0],[1.0,-1.0,0.0],[4.0,-2.0,-1.0]],dtype = numpy.float)
y = array([-4.0,0.0,-6.0],dtype = numpy.float)
print "X",x
print "Y",y
print "linalg", linalg.solve(x,y)
c = gauss(x,y)
print "coeff", c
print "----------------"
x = matrix([[0.0,1.0,1.0],[3.0,2.0,1.0],[1.0,1.0,1.0]],dtype = numpy.float)
y = array([5.0,10.0,6.0],dtype = numpy.float)
print "X",x
print "Y",y
c = gauss(x,y)
print "coeff", c
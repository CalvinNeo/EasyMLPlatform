#coding:utf8

from numpy import *
import numpy

def gauss(a,b):
    n = len(b)
    for i in range(0,n-1):
        for j in range(i+1,n):
            if a[j,i] != 0.0:
                lam = float(a[j,i])/a[i,i]
                a[j,(i+1):n] = a[j,(i+1):n] - lam*a[i,(i+1):n]
                b[j] = b[j] - lam*b[i]
    for k in range(n-1,-1,-1):
        b[k] = (b[k] - dot(a[k,(k+1):n],b[(k+1):n]))/a[k,k]
    result = b
    return result

x = matrix([[2.0,2.0,-1.0],[1.0,-1.0,0.0],[4.0,-2.0,-1.0]],dtype = numpy.float)
y = array([-4.0,0.0,-6.0],dtype = numpy.float)
c = gauss(x,y)

print c
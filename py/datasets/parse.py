#coding:utf8
import sys
sys.path.append('..')

from optparse import OptionParser
import operator
import string
import ast

def parsestr(somethingstring, elselambda=[]):
    x = str(somethingstring)
    if len(x) == 0:
        return None
    if x[0] in list(string.digits)+['-','+','.']:
        try:
            return int(x)
        except ValueError:
            try:
                return float(x)
            except ValueError:
                return x
    elif x.lower() in ['true','false']:
        return True if x.lower() == 'true' else False
    #if not return util now ...
    for lmda in elselambda:
        lr = lmda(x)
        if lr != None:
            return lr
    #ok i can only return a string
    return x
    
def extendboolean(x):
    if x.lower() in ['y', 'yes', 't']:
        return True
    elif x.lower() in ['n', 'no', 'f']:
        return False

if __name__ == '__main__':
    print list(string.digits)+['-','+','.']
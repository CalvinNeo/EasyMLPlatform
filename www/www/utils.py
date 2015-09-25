#coding:utf8

import os,sys,random,time

def random_file_name(name):
    ext = os.path.splitext(name)[1]
    new_name = time.strftime("%Y%m%d%H%M%S")
    new_name = new_name + "_%d"%(random.randint(100,999))
    name = new_name + ext
    return name
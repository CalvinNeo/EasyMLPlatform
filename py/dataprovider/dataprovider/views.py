#coding:utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import MySQLdb
import thread, time, threading, math, random


intervaldata = []
stop_flag = 0
'''
    0: no thread running
    1: one thread running
    2: stop
'''
def intervalmain():
    global stop_flag
    def gaussdist(mean, var):
        u=0.0
        v=0.0
        w=0.0
        c=0.0
        while(w==0.0 or w>=1.0):
            u = random.random()*2-1.0
            v = random.random()*2-1.0
            w = u*u+v*v
        c = ((-2*math.log(w))/w) ** 0.5
        return u*c;
    while True:
        if stop_flag == 1:
            # every 2 sec
            time.sleep(3)
            # print [len(intervaldata), math.sin(len(intervaldata)) + gaussdist(0, 0.1)]
            intervaldata.append( [str(len(intervaldata)), str(math.sin(len(intervaldata)) + gaussdist(0, 0.1))] )
        else:
            print "--stop"
            stop_flag = 0
            return


def index(request, operation = "", *args, **kwargs):
    global stop_flag, intervaldata
    try:
        print intervaldata
        return {
            'guasslin': render(request, "interval.html", {'dimen': 2
            , 'name': ''
            , 'head': ['x', 'sin(x)+noise']
            , 'interval': 2000
            , 'mathfunc': 'function(x){return Math.sin(x)}'
            , 'start': 0
            , 'noisesigma': 0.1
            , 'data': intervaldata
            })
            ,'guasslin_update':HttpResponse( 
                ';'.join( map(lambda x: ','.join(x), intervaldata ) )
            )
        }[operation.decode('utf8')]
    except KeyError:
        if operation.decode('utf8') == 'guasslin_start':
            if stop_flag == 0:
                stop_flag = 1
                intervalthread = threading.Thread(target=intervalmain, args=())
                # args are args given to target
                print '--start'
                intervalthread.start()
            return HttpResponse("")
        elif operation.decode('utf8') == 'guasslin_stop':
            if stop_flag == 1:
                stop_flag = 2
            return HttpResponse("")
        else:
            return render(request, "data.html",{
            'name': 'Iris'
            ,'head':['feature1','feature2','feature3','feature4','class']
            ,'data':[[5.1,3.5,1.4,0.2,1],
                    [4.9,3.0,1.4,0.2,1],
                    [4.7,3.2,1.3,0.2,1],
                    [4.6,3.1,1.5,0.2,1],
                    [5.0,3.6,1.4,0.2,1],
                    [5.4,3.9,1.7,0.4,1],
                    [4.6,3.4,1.4,0.3,1],
                    [5.0,3.4,1.5,0.2,1],
                    [4.4,2.9,1.4,0.2,1],
                    [4.9,3.1,1.5,0.1,1],
                    [5.4,3.7,1.5,0.2,1],
                    [4.8,3.4,1.6,0.2,1],
                    [4.8,3.0,1.4,0.1,1],
                    [4.3,3.0,1.1,0.1,1],
                    [5.8,4.0,1.2,0.2,1],
                    [5.7,4.4,1.5,0.4,1],
                    [5.4,3.9,1.3,0.4,1],
                    [5.1,3.5,1.4,0.3,1],
                    [5.7,3.8,1.7,0.3,1],
                    [5.1,3.8,1.5,0.3,1],
                    [5.4,3.4,1.7,0.2,1],
                    [5.1,3.7,1.5,0.4,1],
                    [4.6,3.6,1.0,0.2,1],
                    [5.1,3.3,1.7,0.5,1],
                    [4.8,3.4,1.9,0.2,1],
                    [5.0,3.0,1.6,0.2,1],
                    [5.0,3.4,1.6,0.4,1],
                    [5.2,3.5,1.5,0.2,1],
                    [5.2,3.4,1.4,0.2,1],
                    [4.7,3.2,1.6,0.2,1],
                    [4.8,3.1,1.6,0.2,1],
                    [5.4,3.4,1.5,0.4,1],
                    [5.2,4.1,1.5,0.1,1],
                    [5.5,4.2,1.4,0.2,1],
                    [4.9,3.1,1.5,0.1,1],
                    [5.0,3.2,1.2,0.2,1],
                    [5.5,3.5,1.3,0.2,1],
                    [4.9,3.1,1.5,0.1,1],
                    [4.4,3.0,1.3,0.2,1],
                    [5.1,3.4,1.5,0.2,1],
                    [5.0,3.5,1.3,0.3,1],
                    [4.5,2.3,1.3,0.3,1],
                    [4.4,3.2,1.3,0.2,1],
                    [5.0,3.5,1.6,0.6,1],
                    [5.1,3.8,1.9,0.4,1],
                    [4.8,3.0,1.4,0.3,1],
                    [5.1,3.8,1.6,0.2,1],
                    [4.6,3.2,1.4,0.2,1],
                    [5.3,3.7,1.5,0.2,1],
                    [5.0,3.3,1.4,0.2,1],
                    [7.0,3.2,4.7,1.4,-1],
                    [6.4,3.2,4.5,1.5,-1],
                    [6.9,3.1,4.9,1.5,-1],
                    [5.5,2.3,4.0,1.3,-1],
                    [6.5,2.8,4.6,1.5,-1],
                    [5.7,2.8,4.5,1.3,-1],
                    [6.3,3.3,4.7,1.6,-1],
                    [4.9,2.4,3.3,1.0,-1],
                    [6.6,2.9,4.6,1.3,-1],
                    [5.2,2.7,3.9,1.4,-1],
                    [5.0,2.0,3.5,1.0,-1],
                    [5.9,3.0,4.2,1.5,-1],
                    [6.0,2.2,4.0,1.0,-1],
                    [6.1,2.9,4.7,1.4,-1],
                    [5.6,2.9,3.6,1.3,-1],
                    [6.7,3.1,4.4,1.4,-1],
                    [5.6,3.0,4.5,1.5,-1],
                    [5.8,2.7,4.1,1.0,-1],
                    [6.2,2.2,4.5,1.5,-1],
                    [5.6,2.5,3.9,1.1,-1],
                    [5.9,3.2,4.8,1.8,-1],
                    [6.1,2.8,4.0,1.3,-1],
                    [6.3,2.5,4.9,1.5,-1],
                    [6.1,2.8,4.7,1.2,-1],
                    [6.4,2.9,4.3,1.3,-1],
                    [6.6,3.0,4.4,1.4,-1],
                    [6.8,2.8,4.8,1.4,-1],
                    [6.7,3.0,5.0,1.7,-1],
                    [6.0,2.9,4.5,1.5,-1],
                    [5.7,2.6,3.5,1.0,-1],
                    [5.5,2.4,3.8,1.1,-1],
                    [5.5,2.4,3.7,1.0,-1],
                    [5.8,2.7,3.9,1.2,-1],
                    [6.0,2.7,5.1,1.6,-1],
                    [5.4,3.0,4.5,1.5,-1],
                    [6.0,3.4,4.5,1.6,-1],
                    [6.7,3.1,4.7,1.5,-1],
                    [6.3,2.3,4.4,1.3,-1],
                    [5.6,3.0,4.1,1.3,-1],
                    [5.5,2.5,4.0,1.3,-1],
                    [5.5,2.6,4.4,1.2,-1],
                    [6.1,3.0,4.6,1.4,-1],
                    [5.8,2.6,4.0,1.2,-1],
                    [5.0,2.3,3.3,1.0,-1],
                    [5.6,2.7,4.2,1.3,-1],
                    [5.7,3.0,4.2,1.2,-1],
                    [5.7,2.9,4.2,1.3,-1],
                    [6.2,2.9,4.3,1.3,-1],
                    [5.1,2.5,3.0,1.1,-1],
                    [5.7,2.8,4.1,1.3,-1]]
            })
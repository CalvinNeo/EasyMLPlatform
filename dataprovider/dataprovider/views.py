#coding:utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import MySQLdb

def index(request, operation = "", *args, **kwargs):
    print "ddd"
    try:
        return {
        }[operation.decode('utf8')]
    except KeyError:
        return render(request,"data.html",{
            'head':['a','b','c']
            ,'data':[[1,2,3],[4,5,6],[7,8,9]]
            })
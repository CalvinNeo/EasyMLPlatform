#coding:utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from www.forms import *

import MySQLdb

# def first_page(request):
#     db = MySQLdb.connect(user='root', db='mlplatform', passwd='80868086', host='localhost')
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM dataset ORDER BY id')
#     names = [row[0] for row in cursor.fetchall()]
#     db.close()
#     return render_to_response('list.html', {'names': names})

def index(request,operation = ""):
    try:
        return {'dataset': render(request,"ds_list.html")
         ,'model': render(request,"404.html",{'title':'Not Completed'})
         ,'analysis': render(request,"404.html",{'title':'Not Completed'})
        }[operation]
    except KeyError:
        if operation == "dataset_upload":
            if request.method == "POST":
                form = UploadDatasetForm(request.POST)
                if form.is_valid():
                    pass
                else:
                    return render(request,"error.html",{'title':'invalid dataset','description':''})
            else:
                form = UploadDatasetForm()
                return render(request,"ds_upload.html",{'form':form})
        else:
            return render(request,"404.html",{'title':'Page Not Found'})
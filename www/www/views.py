#coding:utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from www.forms import *
from www.models import *

import MySQLdb

# def first_page(request):
#     db = MySQLdb.connect(user='root', db='mlplatform', passwd='80868086', host='localhost')
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM dataset ORDER BY id')
#     names = [row[0] for row in cursor.fetchall()]
#     db.close()
#     return render_to_response('list.html', {'names': names})
def api(request, operation = "", *args, **kwargs):
    pass
def index(request, operation = "", *args, **kwargs):
    print operation
    try:
        return {'dataset': render(request,"dataset.html",{
            'datasets':Dataset.GetDatasets(),
            'select':False,'operation':True })
         ,'model': render(request,"404.html",{'title':'Not Completed'})
         ,'apply': render(request,"404.html",{'title':'Not Completed'})
         ,'accessment': render(request,"404.html",{'title':'Not Completed'})
         #Partial
         ,'dataset_view':render(request,"ds_view.html",{'dataset':Dataset.ViewDataset(unicodedatasetindex=request.GET.get('datasetindex'))})
        }[operation]
    except KeyError:
        #form action
        if operation == "dataset_upload":
            if request.method == "POST":
                form = UploadDatasetForm(request.POST,request.FILES)
                if form.is_valid():
                    ds = Dataset()
                    ds.name = str(form.cleaned_data['name'])
                    ds.path = form.cleaned_data['datasetfile']
                    ds.filetype = str(form.cleaned_data['filetype'])
                    ds.head = '1,2,3'
                    ds.attr_delim = ','
                    ds.record_delim = '\n'
                    ds.save()
                    return render(request,"success.html",{'title':'upload dataset succeed!','description':str(form.cleaned_data['name'])})
                else:
                    return render(request,"error.html",{'title':'invalid dataset','description':str(form.cleaned_data['name']) + " " +str(form.cleaned_data['datasetfile']).decode('utf8')})
            else:
                form = UploadDatasetForm()
                return render(request,"ds_upload.html",{'form':form})
        elif operation == "model_upload":
            if request.method == "POST":
                pass
            else:
                pass
        else:
            return render(request,"404.html",{'title':'Page Not Found'})
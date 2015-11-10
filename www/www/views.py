#coding:utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from www.forms import *
from www.models import *
import MySQLdb

import datasets.localdata

# def first_page(request):
#     db = MySQLdb.connect(user='root', db='mlplatform', passwd='80868086', host='localhost')
#     cursor = db.cursor()
#     cursor.execute('SELECT * FROM dataset ORDER BY id')
#     names = [row[0] for row in cursor.fetchall()]
#     db.close()
#     return render_to_response('list.html', {'names': names})
def api(request, operation = "", *args, **kwargs):
    print "api:",operation
    print request.GET.get('datasetindex')
    return {
        '': HttpResponse("")
        ,'dataset_delete': HttpResponse(Dataset.DeleteDataset(unicodedatasetindex=request.GET.get('datasetindex')))
    }[operation]

def index(request, operation = "", *args, **kwargs):
    print "index:",operation
    try:
        return {'dataset': render(request,"dataset.html",{
            'datasets':Dataset.GetDatasets(),
            'select':True,'operation':True })
         ,'models': render(request,"trainmodel.html",{
            })
         ,'apply': render(request,"404.html",{'title':'Not Completed'})
         ,'accessment': render(request,"404.html",{'title':'Not Completed'})
         #Partial
         ,'ds_view':render(request,"ds_view.html",{'dataset':Dataset.ViewDataset(unicodedatasetindex=request.GET.get('datasetindex'))})
        }[operation.decode('utf8')]
    except KeyError:
        #form action
        if operation == "dataset_upload":
            if request.method == "POST":
                form = UploadDatasetForm(request.POST,request.FILES)
                if form.is_valid():
                    ds = Dataset()
                    ds.name = str(form.cleaned_data['name'])
                    ds.path = form.cleaned_data['datasetfile']
                    ds.filetype = {
                        'txt':'TXT',
                        'csv':'CSV',
                        'xls':'XLS',
                    }[str(ds.path).split('.')[-1].lower()]
                    #head shows if the dataset has head
                    ds.head = ""#str(form.cleaned_data['hashead']))
                    print '-------------',str(form.cleaned_data['attr_delim'])
                    ds.attr_delim = ',' if str(form.cleaned_data['attr_delim']) == '' else str(form.cleaned_data['attr_delim']).replace('\\n','\n').replace('\\t','\t')
                    ds.record_delim = '\n' if str(form.cleaned_data['record_delim']) == '' else str(form.cleaned_data['record_delim']).replace('\\n','\n').replace('\\t','\t')
                    ds.save()
                    return render(request,"success.html",{'title':'upload dataset succeed!','description':str(form.cleaned_data['name']).decode('utf8')})
                else:
                    return render(request,"error.html",{'title':'invalid dataset','description':str(form.cleaned_data['name']).decode('utf8')+" "})
            else:
                form = UploadDatasetForm()
                return render(request,"ds_upload.html",{'form':form})
        elif operation == "model_new":
            if request.method == "POST":
                pass
            else:
                pass
        elif operation == "model_view":
            pass
        else:
            return render(request,"404.html",{'title':'Page Not Found'})


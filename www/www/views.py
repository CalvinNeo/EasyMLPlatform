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
            'distributed_modeltypes':MLModel.AllDistributedModels()
            ,'modeltypes':MLModel.AllModels()
            ,'select':True,'operation':True
            })
         ,'apply': render(request,"404.html",{'title':'Not Completed'})
         ,'assessment': render(request,"assessmodel.html",{})
         #Partial
         ,'ds_view':render(request,"ds_view.html",{'dataset':Dataset.ViewDataset(unicodedatasetindex=request.GET.get('datasetindex'))})
        }[operation.decode('utf8')]
    except KeyError:
        #form action
        if operation == "dataset_upload":
            if request.method == "POST":
                form = UploadDatasetForm(request.POST,request.FILES)
                print "-----------------------------aa"
                print dir(form)
                print form.data
                print form.errors
                if form.is_valid():
                    ds = Dataset()
                    print "-----------------------------bb"
                    ds.name = str(form.cleaned_data['name'])
                    # if 'dataseturl' in form.cleaned_data.keys():
                        # ds.type = 1
                        # ds.path = form.cleaned_data['dataseturl']
                        # ds.filetype = ""
                        # ds.head = ""
                        # ds.attr_delim = ""
                        # ds.record_delim = ""
                        # ds.location = form.cleaned_data['location']
                        # ds.search = form.cleaned_data['search']
                    # else:
                    # ds.type = 0
                    ds.path = form.cleaned_data['datasetfile']
                    ds.filetype = {
                        'txt':'TXT',
                        'csv':'CSV',
                        'xls':'XLS',
                    }[str(ds.path).split('.')[-1].lower()]
                    #head shows if the dataset has head
                    ds.head = ""
                    ds.attr_delim = ',' if str(form.cleaned_data['attr_delim']) == '' else str(form.cleaned_data['attr_delim']).replace('\\n','\n').replace('\\t','\t')
                    ds.record_delim = '\n' if str(form.cleaned_data['record_delim']) == '' else str(form.cleaned_data['record_delim']).replace('\\n','\n').replace('\\t','\t')
                    # ds.location = ""
                    # ds.search = ""
                        
                    ds.save()
                    return render(request,"success.html",{'title':'upload dataset succeed!','description':str(form.cleaned_data['name']).decode('utf8')})
                else:
                    return render(request,"error.html",{'title':'invalid dataset','description':form.errors})
            else:
                form = UploadDatasetForm()
                return render(request,"ds_upload.html",{'form':form})
        elif operation == "md_new":
            if request.method == "POST":
                pass
            else:
                return render(request,"md_new.html",{
                    'distributed_modeltypes':str(MLModel.AllDistributedModels())
                    ,'modeltypes':str(MLModel.AllModels())
                    })
        elif operation == "model_view":
            pass
        else:
            return render(request,"404.html",{'title':'Page Not Found'})


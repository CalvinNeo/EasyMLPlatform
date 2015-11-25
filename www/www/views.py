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
    operation = str(operation)
    if operation == "dataset_delete":
        return HttpResponse(Dataset.DeleteDataset(unicodedatasetindex=request.GET.get('datasetindex')))
    elif operation == "oldataset_delete":
        return HttpResponse(OnlineDataset.DeleteDataset(unicodedatasetindex=request.GET.get('datasetindex')))
    else:
        return HttpResponse("")

def index(request, operation = "", *args, **kwargs):
    print "--------------------index:",operation,request.GET
    #特别注意一点,{}[p]这种选择方式,dict里面是全部求值的
    try:
        return {'dataset': render(request,"dataset.html",{
            'datasets':Dataset.GetDatasets()
            ,'oldatasets':OnlineDataset.GetDatasets()
            ,'renewstrategies':OnlineDataset.AllRenewStrategies()
            ,'select':True,'operation':True 
            })
         ,'models': render(request,"trainmodel.html",{
            'distributed_modeltypes':MLModel.AllDistributedModels()
            ,'modeltypes':MLModel.AllModels()
            ,'select':True,'operation':True
            })
         ,'apply': render(request,"404.html",{'title':'Not Completed'})
         ,'assessment': render(request,"assessmodel.html",{})

         #util
         ,'302':render(request,"302.html",{'url':request.GET.get('url')
            ,'time':0 if request.GET.get('time')==None else request.GET.get('time')
            })
        }[operation.decode('utf8')]
    except KeyError:
        #form action
        if operation == "dataset_upload":
            if request.method == "POST":
                form = UploadDatasetForm(request.POST,request.FILES)
                print "-----------------------------aa"
                # print "request.META", request.META
                print "files", form.files
                print "form.data",form.data
                print "ERRORS:", form.errors
                print "FILES", request.FILES
                print "form.is_valid()",form.is_valid()
                if form.is_valid():
                    ds = Dataset()
                    ds.name = str(form.cleaned_data['name'])
                    ds.path = form.cleaned_data['path']
                    ds.filetype = {
                        'txt':'TXT',
                        'csv':'CSV',
                        'xls':'XLS',
                    }[str(ds.path).split('.')[-1].lower()]
                    #head shows if the dataset has head
                    ds.head = ""
                    ds.attr_delim = ',' if str(form.cleaned_data['attr_delim']) == '' else str(form.cleaned_data['attr_delim']).replace('\\n','\n').replace('\\t','\t')
                    ds.record_delim = '\n' if str(form.cleaned_data['record_delim']) == '' else str(form.cleaned_data['record_delim']).replace('\\n','\n').replace('\\t','\t')
                    ds.save()
                    return render(request,"success.html",{'title':'upload dataset succeed!','description':str(form.cleaned_data['name']).decode('utf8')})
                else:
                    return render(request,"error.html",{'title':'invalid dataset','description':form.errors})
            else:
                form = UploadDatasetForm()
                return render(request,"ds_upload.html",{
                    'form':form
                    ,'renewstrategies':OnlineDataset.AllRenewStrategies()
                    })
        elif operation == "onlinedataset_upload":
            if request.method == "POST":
                form = OnlineDatasetForm(request.POST,request.FILES)
                if form.is_valid():
                    ds = OnlineDataset()
                    ds.name = str(form.cleaned_data['name'])
                    ds.url = form.cleaned_data['url']
                    ds.location = 'table' if str(form.cleaned_data['location']) == '' else str(form.cleaned_data['location']).replace('\\n','\n').replace('\\t','\t')
                    ds.search = '' if str(form.cleaned_data['location']) == '' else str(form.cleaned_data['location']).replace('\\n','\n').replace('\\t','\t')
                    ds.save()
                    return render(request,"success.html",{'title':'upload online dataset succeed!','description':str(form.cleaned_data['name']).decode('utf8')})
                else:
                    return render(request,"error.html",{'title':'invalid online dataset','description':form.errors})
            else:
                form = OnlineDatasetForm()
                return render(request,"olds_upload.html",{
                    'form':form
                    ,'renewstrategies':OnlineDataset.AllRenewStrategies()
                    })
        elif operation == 'ds_view':
            return render(request,"ds_view.html",{
                'dataset':Dataset.ViewDataset(unicodedatasetindex=request.GET.get('datasetindex'))
                })
        elif operation == 'olds_view':
            return render(request,"olds_view.html",{
                'dataset':OnlineDataset.ViewDataset(unicodedatasetindex=request.GET.get('datasetindex'))
                })
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


#coding:utf8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect

import MySQLdb
import json

import datasets.localdata
from www.forms import *
from www.models import *

from django.contrib.auth.models import User    
from django.contrib import auth  
from django.contrib import messages  
from django.contrib.auth.decorators import login_required   
import settings

def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def HTTPS_Response(request, URL):
    if settings.SERVER_TYPE == "DEV":
        new_URL = URL
    else:
        absolute_URL = request.build_absolute_uri(URL)
        new_URL = "https%s" % absolute_URL[4:]
    return HttpResponseRedirect(new_URL)

def httpstest(request):
    return HttpResponse('AHHHHH')

def api(request, operation = "", *args, **kwargs):
    print "api:",operation
    operation = str(operation)
    if operation == "dataset_delete":
        return HttpResponse(Dataset.DeleteDataset(unicodedatasetindex=request.GET.get('datasetindex')))
    elif operation == "oldataset_delete":
        return HttpResponse(OnlineDataset.DeleteDataset(unicodedatasetindex=request.GET.get('datasetindex')))
    elif operation == 'onlinedataset_dump':
        return HttpResponse(OnlineDataset.DumpDataset(unicodedatasetindex=request.GET.get('datasetindex')))
    elif operation == 'model_delete':
        return HttpResponse(MLModel.DeleteModel(unicodemodelindex=request.GET.get('modelindex'))) 
    elif operation == 'model_view':
        return HttpResponse( repr(MLModel.ViewModel(unicodemodelindex=request.GET.get('modelindex'))) )
    elif operation == 'dataset_view':
        return HttpResponse( repr(Dataset.GetDataset(unicodedatasetindex=request.GET.get('datasetindex'))) )
    elif operation == 'oldataset_view':
        return HttpResponse( repr(OnlineDataset.GetDataset(unicodedatasetindex=request.GET.get('datasetindex'))) )
    elif operation == 'dataset_list':
        return HttpResponse( repr(Dataset.GetDatasets()) )
    elif operation == 'oldataset_list':
        return HttpResponse( repr(OnlineDataset.GetDatasets()) )
    elif operation == 'task_delete':
        return HttpResponse( repr(TrainingTask.DeleteTask(unicodetaskindex=request.GET.get('taskindex'))) )
    elif operation == 'hash_image':
        imgname = str(request.POST.get('name'))
        action = str(request.POST.get('id'))
        if action in ['ROC']:
            return HttpResponse("true")
        elif action in ['Dataset']:
            return HttpResponse("true")
        elif action == 'absolute':
            return HttpResponse("true")
    elif operation == 'mdimage':
        return HttpResponse(MLModel.GetImage(unicodemodelindex=request.GET.get('modelindex')))
    elif operation == 'dsimage':
        return HttpResponse(Dataset.GetImage(unicodedatasetindex=request.GET.get('datasetindex'))) 
    elif operation == 'oldsimage':
        return HttpResponse(OnlineDataset.GetImage(unicodedatasetindex=request.GET.get('datasetindex'))) 
    elif operation == 'model_train':
        return HttpResponse(TrainingTask.CreateTrain(unicodemodelindex=request.GET.get('modelindex'))) 
    elif operation == 'model_apply':
        applytask = ApplyTask.CreateApply(unicodemodelindex=request.GET.get('modelindex')
            , unicodedatasetindex=request.GET.get('datasetindex')
            , unicodeoldatasetindex=request.GET.get('oldatasetindex')
            , unicodeselectwhichdatasettype=request.GET.get('selectwhichdatasettype')
            , unicoderemove=request.GET.get('removeitem')
            )
        resultdataset = applytask.Start()
        # save dataset and print out
        return render(request,"ds_view.html",{'dataset':resultdataset})
    elif operation == 'model_assess':
        assesstask = AssessTask.CreateAssess(unicodemodelindex=request.GET.get('modelindex')
            , unicodedatasetindex=request.GET.get('datasetindex')
            , unicodeoldatasetindex=request.GET.get('oldatasetindex')
            , unicodeselectwhichdatasettype=request.GET.get('selectwhichdatasettype')
            , unicodeclassfeatureindex=request.GET.get('classfeatureindex')
            , unicodeassessmethod=request.GET.get('assessmethod')
            )
        assessmodel = assesstask.Start()
        if assessmodel.Protoclass == 'REGRESS':
            pass
        elif assessmodel.Protoclass == 'CLUSTER':
            pass
        elif assessmodel.Protoclass == 'CLASSIFY':
            json_stuff = json.dumps([
                {'name':'TP', 'value':assessmodel.TP}
                ,{'name':'TN', 'value':assessmodel.TN}
                ,{'name':'FP', 'value':assessmodel.FP}
                ,{'name':'FN', 'value':assessmodel.FN}
                ,{'name':'P', 'value':assessmodel.P}
                ,{'name':'R', 'value':assessmodel.R}
                ,{'name':'F1', 'value':assessmodel.F1}
            ])
            return HttpResponse(json_stuff, content_type ="application/json")
        else:
            pass
    else:
        return HttpResponse("")

def users(request, operation = "", *args, **kwargs):
    operation = str(operation)
    if operation == 'create':
        user = User.objects.create_user(str(request.GET.get('name')), str(request.GET.get('email')), str(request.GET.get('password')))
    elif operation == 'chpass':
        User.objects.get(username=str(request.GET.get('name')).set_password('password'))
    elif operation == 'auth':
        user = authenticate(username=str(request.GET.get('name')), password=str(request.GET.get('password')))
        if user is not None:
            if user.is_active:
                return HttpResponse("false")
            else:
                # the account is disabled
                return HttpResponse("false")
        else:
            return HttpResponse("false")
    return HttpResponse("true")

def login(request, *args, **kwargs):
    if request.method == 'GET':  
        form = LoginForm()  
        return render(request, 'index.html', {'form': form,})  
    else:  
        form = LoginForm(request.POST)  
        if form.is_valid():  
            username = request.POST.get('username', '')  
            password = request.POST.get('password', '')  
            user = auth.authenticate(username=username, password=password)  
            if user is not None and user.is_active:  
                auth.login(request, user)  
                return HttpResponseRedirect("/index/dataset/")  
            else:  
                return render(request, 'index.html', {'form': form,'password_is_wrong':True})  
        else:  
            return render(request, 'index.html', {'form': form})

def logout(request, *args, **kwargs):
    auth.logout(request)  
    return HttpResponseRedirect("/login/")  

@login_required
def index(request, operation = "", *args, **kwargs):
    #特别注意一点,{}[p]这种选择方式,dict里面是全部求值的
    try:
        return {
         #util
         '302':render(request,"302.html",{'url':request.GET.get('url')
            ,'time':0 if request.GET.get('time')==None else request.GET.get('time')
            })
         ,'':render(request,"index.html")
        }[operation.decode('utf8')]
    except KeyError:
        #form action
        if operation == 'dataset':
            return render(request,"dataset.html",{
                'datasets':Dataset.GetDatasets()
                ,'oldatasets':OnlineDataset.GetDatasets()
                ,'renewstrategies':OnlineDataset.AllRenewStrategies()
                ,'operation':operation
                ,'ds_select':True, 'ds_operation':True, 'ds_delete':True, 'ds_choose':False, 'ds_show':True
                ,'md_select':True, 'md_operation':True, 'md_delete':True, 'md_choose':False, 'md_show':False, 'md_train':False
                })
        elif operation == 'models':
            return render(request,"trainmodel.html",{            
                'datasets':Dataset.GetDatasets()
                ,'oldatasets':OnlineDataset.GetDatasets()
                ,'distributed_modeltypes':MLModel.AllDistributedModels()
                ,'modeltypes':MLModel.AllModels()
                ,'models': MLModel.GetModels()
                ,'tasks':TrainingTask.GetTasks()
                ,'operation':operation
                ,'ds_select':False, 'ds_operation':True, 'ds_delete':False, 'ds_choose':True, 'ds_show':False
                ,'md_select':True, 'md_operation':True, 'md_delete':True, 'md_choose':True, 'md_show':True, 'md_train':True
                })
        elif operation == 'apply':
            return render(request,"applymodel.html",{
                'distributed_modeltypes':MLModel.AllDistributedModels()
                ,'modeltypes':MLModel.AllModels()
                ,'models': MLModel.GetModels()
                ,'datasets':Dataset.GetDatasets()
                ,'oldatasets':OnlineDataset.GetDatasets()
                ,'operation':operation
                ,'ds_select':False, 'ds_operation':True, 'ds_delete':False, 'ds_choose':True, 'ds_show':True
                ,'md_select':False, 'md_operation':True, 'md_delete':False, 'md_choose':True, 'md_show':True, 'md_train':False
                })
        elif operation == 'assessment':
            return render(request,"assessmodel.html",{
                'distributed_modeltypes':MLModel.AllDistributedModels()
                ,'modeltypes':MLModel.AllModels()
                ,'models': MLModel.GetModels()
                ,'datasets':Dataset.GetDatasets()
                ,'oldatasets':OnlineDataset.GetDatasets()
                ,'operation':operation
                ,'assessmethods':[]
                ,'ds_select':False, 'ds_operation':True, 'ds_delete':False, 'ds_choose':True, 'ds_show':False
                ,'md_select':False, 'md_operation':True, 'md_delete':False, 'md_choose':True, 'md_show':False, 'md_train':False
                })
        elif operation == "dataset_upload":
            if request.method == "POST":
                form = UploadDatasetForm(request.POST,request.FILES)
                # print "request.META", request.META
                print "files", form.files
                print "form.data",form.data
                print "ERRORS:", form.errors
                print "FILES", request.FILES
                print "form.is_valid()",form.is_valid()
                print request
                print request.user
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
                    ds.head = str(form.cleaned_data['head'])
                    ds.hashead = bool(form.cleaned_data['hashead'])
                    ds.attr_delim = ',' if str(form.cleaned_data['attr_delim']) == '' else str(form.cleaned_data['attr_delim']).replace('\\n','\n').replace('\\t','\t')
                    ds.record_delim = '\n' if str(form.cleaned_data['record_delim']) == '' else str(form.cleaned_data['record_delim']).replace('\\n','\n').replace('\\t','\t')
                    ds.user = str(request.user)
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
                    ds.renewstrategy = str(form.cleaned_data['renewstrategy'])
                    ds.metatype = str(form.cleaned_data['metatype'])
                    ds.head = str(form.cleaned_data['head'])
                    ds.hashead = bool(form.cleaned_data['hashead'])
                    ds.location = 'table' if str(form.cleaned_data['location']) == '' else str(form.cleaned_data['location']).replace('\\n','\n').replace('\\t','\t')
                    ds.search = '' if str(form.cleaned_data['search']) == '' else str(form.cleaned_data['search']).replace('\\n','\n').replace('\\t','\t')
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
                form = NewModelForm(request.POST,request.FILES)
                if form.is_valid():
                    mm = MLModel()
                    mm.name = str(form.cleaned_data['name'])
                    mm.modeltype = str(form.cleaned_data['modeltype'])
                    mm.classfeatureindex = int(form.cleaned_data['classfeatureindex'])
                    selectwhichdatasettype = str(form.cleaned_data['selectwhichdatasettype'])
                    if selectwhichdatasettype == 'ds':
                        mm.datasetprototype = 'LOCAL'
                        mm.datasetindex = int(form.cleaned_data['datasetindex'])
                    elif selectwhichdatasettype == 'ol':
                        mm.datasetprototype = 'ONLINE'
                        mm.datasetindex = int(form.cleaned_data['oldatasetindex'])
                    else:
                        pass
                    mm.modelstatus = 'INITED'
                    mm.save()
                    return render(request,"success.html",{'title':'create new model succeed!','description':str(form.cleaned_data['name']).decode('utf8')})
                else:
                    return render(request,"error.html",{'title':'invalid model','description':form.errors})
            else:
                return render(request,"md_new.html",{
                    'distributed_modeltypes':str(MLModel.AllDistributedModels())
                    ,'modeltypes':str(MLModel.AllModels())
                    })
        elif operation == "md_view":
            md = MLModel.GetModels(unicodedatasetindex=request.GET.get('modelindex'))
        elif operation == "node_manager":
            return HttpResponseRedirect('http://localhost:8190/inspinia/')
            # return render(request,"node_manager.html",{})
        else:
            return render(request,"404.html",{'title':'Page Not Found'})


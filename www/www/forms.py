#coding:utf8

from django import forms

class UploadDatasetForm(forms.Form):
    name = forms.CharField(max_length = 20)
    datasetfile = forms.FileField()
    hashead = forms.CharField(max_length=10,required=False)  
    attr_delim = forms.CharField(max_length = 3,required=False)
    record_delim = forms.CharField(max_length = 3,required=False)

class NewModelForm(forms.Form):
    name = forms.CharField(max_length = 20)
    modeltype = forms.CharField(max_length=10) 
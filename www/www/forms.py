#coding:utf8

from django import forms

class UploadDatasetForm(forms.Form):
    name = forms.CharField(max_length = 20)
    datasetfile = forms.FileField()
    hashead = forms.CharField(max_length=10)  
    attr_delim = forms.CharField(max_length = 3)
    record_delim = forms.CharField(max_length = 3)

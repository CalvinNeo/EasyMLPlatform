#coding:utf8

from django import forms

class UploadDatasetForm(forms.Form):
    name = forms.CharField(max_length=20)
    path = forms.FileField(required=True)
    attr_delim = forms.CharField(max_length=3,required=False)
    record_delim = forms.CharField(max_length=3,required=False)
    head = forms.CharField(max_length=1023,required=False)
    hashead = forms.BooleanField(required=False)

class OnlineDatasetForm(forms.Form):
    name = forms.CharField(max_length=20)
    #if you use lambda here you can't pass migration, 因为lambda不能被序列化! 
    url = forms.CharField(200)
    location = forms.CharField(max_length=1023,required=False)
    search = forms.CharField(max_length=1023,required=False)
    renewstrategy = forms.CharField(max_length=32,required=False)
    head = forms.CharField(max_length=1023,required=False)
    hashead = forms.BooleanField(required=False)

class NewModelForm(forms.Form):
    name = forms.CharField(max_length = 20)
    modeltype = forms.CharField(max_length= 32) 
    classfeatureindex = forms.IntegerField(required=False) 

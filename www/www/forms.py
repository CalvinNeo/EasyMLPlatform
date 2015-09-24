#coding:utf8

from django import forms

class UploadDatasetForm(forms.Form):
	name = forms.CharField(max_length=20)
	
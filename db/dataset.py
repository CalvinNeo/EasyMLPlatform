#coding:utf8

from django.db import models

class Dataset(models.Model):
	id = models.IntegerField()
	name = models.CharField(max_length=20)
	path = models.CharField(max_length=255)
	filetype = models.CharField(max_length=10) 	
	head = models.CharField(max_length=1023)
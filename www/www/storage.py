#coding:utf8
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.conf import settings

from www.utils import random_file_name

class FileStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        #初始化
        super(FileStorage, self).__init__(location, base_url)
 
    #重写 _save方法        
    def _save(self, name, content, subclass):
        #调用父类方法
        return super(FileStorage, self)._save('./upload/' + random_file_name(name), content)
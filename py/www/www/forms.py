#coding:utf8

from django import forms

class UploadDatasetForm(forms.Form):
    # modify use
    datasetindex = forms.IntegerField(required=False)

    name = forms.CharField(max_length=20)
    path = forms.FileField(required=True)
    attr_delim = forms.CharField(max_length=3,required=False)
    record_delim = forms.CharField(max_length=3,required=False)
    head = forms.CharField(max_length=1023,required=False)
    hashead = forms.BooleanField(required=False)

class OnlineDatasetForm(forms.Form):
    # modify use
    oldatasetindex = forms.IntegerField(required=False)

    name = forms.CharField(max_length=20)
    # if you use lambda here you can't pass migration, 因为lambda不能被序列化! 
    url = forms.CharField(200)
    location = forms.CharField(max_length=1023,required=False)
    search = forms.CharField(max_length=1023,required=False)
    renewstrategy = forms.CharField(max_length=32,required=False)
    metatype = forms.CharField(max_length=32)
    head = forms.CharField(max_length=1023,required=False)
    hashead = forms.BooleanField(required=False)

class NewModelForm(forms.Form):
    # modify use
    datasetindex = forms.IntegerField(required=False)
    oldatasetindex = forms.IntegerField(required=False)
    modelindex = forms.IntegerField(required=False)

    name = forms.CharField(max_length = 20)
    modeltype = forms.CharField(max_length= 32) 
    oldatasetindex = forms.IntegerField(required=False)
    datasetindex = forms.IntegerField(required=False)
    selectwhichdatasettype = forms.CharField(max_length = 20)

    classfeatureindex = forms.IntegerField(required=False) 
    loss = forms.CharField(required=False) 
    positive = forms.FloatField(required=False)
    negative = forms.FloatField(required=False)

class LoginForm(forms.Form):
    username = forms.CharField(  
        required=True,  
        # label=u"用户名",  
        error_messages={'required': 'username required'},  
        widget=forms.TextInput(  
            attrs={  
                'placeholder':"username",  
            }  
        ),  
    )      
    password = forms.CharField(  
        required=True,  
        # label=u"密码",  
        error_messages={'required': 'password required'},  
        widget=forms.PasswordInput(  
            attrs={  
                'placeholder':"password",  
            }  
        ),  
    )     
    def clean(self):  
        if not self.is_valid():  
            raise forms.ValidationError(u"用户名和密码为必填项")  
        else:  
            cleaned_data = super(LoginForm, self).clean()   


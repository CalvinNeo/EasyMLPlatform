from django.contrib import admin
from www.models import Dataset
from www.models import MLModel
from www.models import OnlineDataset

admin.site.register(Dataset)
admin.site.register(MLModel)
admin.site.register(OnlineDataset)
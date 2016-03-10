from django.contrib import admin
from www.models import Dataset
from www.models import MLModel
from www.models import OnlineDataset
from www.models import TrainingTask

admin.site.register(Dataset)
admin.site.register(MLModel)
admin.site.register(OnlineDataset)
admin.site.register(TrainingTask)
import inspect

from django.db import models as dj_models
from django.contrib import admin

# Register your models here.

from . import models

model_list = [class_name for _, class_name in inspect.getmembers(models)
               if inspect.isclass(class_name)
                 and issubclass(class_name, models.BaseModel)]

admin.site.register([class_ for class_ in model_list if class_ != models.BaseModel])

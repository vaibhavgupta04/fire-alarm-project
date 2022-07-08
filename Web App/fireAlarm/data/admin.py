from django.contrib import admin

# Register your models here.
from .models import request_access_model, sensor_info
admin.site.register(sensor_info)
admin.site.register(request_access_model)
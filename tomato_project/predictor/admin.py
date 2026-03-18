from django.contrib import admin
from .models import UploadedImage, ProgressRecord

admin.site.register(UploadedImage)
admin.site.register(ProgressRecord)

from django.db import models
from django.contrib.auth.models import User

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title or 'Image'} ({self.id})"

class ProgressRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    previous = models.ForeignKey(UploadedImage, related_name='prev_records', on_delete=models.CASCADE)
    latest = models.ForeignKey(UploadedImage, related_name='latest_records', on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Progress {self.id} for {self.user}"

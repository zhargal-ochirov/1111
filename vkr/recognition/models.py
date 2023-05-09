from django.db import models

# Create your models here.

class Data(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True)

    def save(self, *args, **kwargs):
        self.url = self.document.url
        super(Data, self).save(*args, **kwargs)

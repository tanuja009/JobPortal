from django.db import models

# Create

class uploadedfile(models.Model):
  file=models.FileField(upload_to='uploads/')
  upload_at=models.DateField(auto_now_add=True)

  def __str__(self):
    return self.file.name
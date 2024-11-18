from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)  # File name
    content = models.BinaryField()  # Binary file data
    content_type = models.CharField(max_length=100)  # File MIME type
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.name
from django.db import models

class RequestResponse(models.Model):
    method = models.CharField(max_length=10)  # To store HTTP method like GET, POST, etc.
    url = models.URLField(max_length=255)  # To store the URL
    headers = models.JSONField(default=None)
    request = models.JSONField(default=None)
    response = models.JSONField(default=None)  # To store the response data (use JSONField to store structured data)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the entry is created



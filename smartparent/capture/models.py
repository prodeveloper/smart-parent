from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CapturedEvent(models.Model):
    """
    Will contain the information captured from the text
    Will have the normal event fields ie the 
    - event name and description
    - date time
    - source text
    - owner
    """
    event_name = models.CharField(max_length=255)
    event_description = models.TextField()
    event_date_time = models.DateTimeField()
    source_text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.contrib.auth.models import User
from django.db import models


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    
    openai_key = models.CharField(max_length=100, blank=True, default="")
    
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "settings"

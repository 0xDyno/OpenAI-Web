from django.contrib.auth.models import User
from django.db import models


class Settings(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    
    openai_key = models.CharField(blank=True, null=True, max_length=100)
    
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "settings"

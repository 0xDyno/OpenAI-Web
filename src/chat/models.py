from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    prompt = models.TextField()
    accuracy = models.IntegerField()
    model = models.CharField(max_length=50, null=True)
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Conversation on date {self.created} - by user - {self.user} - with id - {self.id}"
    
    class Meta:
        db_table = "conversations"

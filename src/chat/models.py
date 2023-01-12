from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    prompt = models.TextField()
    answer = models.TextField()
    accuracy = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.created}\n\t" \
               f"Prompt: {self.prompt}\n\t" \
               f"Answer: {self.answer}"
    
    class Meta:
        db_table = "conversations"

from django.contrib.auth.models import User
from django.db import models


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=models.deletion.CASCADE)
    
    openai_key = models.CharField(max_length=100, blank=True, default="")
    
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "User {} (id {}) - settings id".format(self.user.username, self.user.id, self.id)
    
    class Meta:
        db_table = "settings"


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


class GeneratedImageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    prompt = models.TextField()
    image = models.ImageField(upload_to="web/static/images")
    path = models.CharField(max_length=200, default="images/")
    
    resolution = models.CharField(max_length=9)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Image (id {}), size = {}, user = {}".format(self.id, self.resolution, self.user)
    
    def delete(self, **kwargs):
        from os import remove
        remove(self.image.name)
        super().delete()
    
    class Meta:
        db_table = "images"

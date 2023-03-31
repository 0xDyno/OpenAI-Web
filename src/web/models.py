from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE


class Settings(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    
    openai_key = models.CharField(max_length=100, blank=True, default="")
    
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "User {} (id {}) - settings id".format(self.user.username, self.user.id, self.id)
    
    class Meta:
        db_table = "settings"


class TextModel(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)
    
    prompt = models.TextField()
    accuracy = models.IntegerField()
    model = models.CharField(max_length=50, null=True)
    response = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"TextModel on date {self.created} - by user - {self.user} - with id - {self.id}"
    
    class Meta:
        db_table = "texts"
        
        
class ChatModel(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)

    name = models.CharField(max_length=50, blank=True)
    alt_info = models.CharField(max_length=150, blank=True)
    last_used = models.CharField(max_length=100, blank=True)
    total_used = models.CharField(max_length=100, blank=True)
    model = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ChatModel {self.id}, \"{self.name}\" ({self.created.date()}) | {self.user}, id {self.user.id}"
    
    class Meta:
        db_table = "chats"
        
        
class Message(models.Model):
    chat = models.ForeignKey(ChatModel, on_delete=CASCADE)
    
    role = models.CharField(max_length=20)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.id} (chat {self.chat.id}, role {self.role})"
    
    class Meta:
        db_table = "messages"


class GeneratedImageModel(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    
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

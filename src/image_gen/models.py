from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    prompt = models.TextField()
    image = models.ImageField()
    size = models.CharField(max_length=9)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Image, size = {}, \nPrompt: {}".format(self.size, self.prompt)
    
    class Meta:
        db_table = "images"

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class ImageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    prompt = models.TextField()
    image = models.ImageField(upload_to="image_gen/static/images")
    resolution = models.CharField(max_length=9)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "Image, size = {}, \nPrompt: {}".format(self.resolution, self.prompt)
    
    class Meta:
        db_table = "images"

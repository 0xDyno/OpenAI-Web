from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class GeneratedImageModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    prompt = models.TextField()
    image = models.ImageField(upload_to="image_gen/static/images")
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

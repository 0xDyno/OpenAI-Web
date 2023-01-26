from django.contrib import admin

from .models import Conversation
from .models import GeneratedImageModel
from .models import Settings

admin.site.register(Conversation)
admin.site.register(GeneratedImageModel)
admin.site.register(Settings)

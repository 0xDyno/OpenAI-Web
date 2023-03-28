from django.contrib import admin

from .models import ChatModel
from .models import Message
from .models import TextModel

from .models import GeneratedImageModel

from .models import Settings

admin.site.register(ChatModel)
admin.site.register(Message)
admin.site.register(TextModel)

admin.site.register(GeneratedImageModel)

admin.site.register(Settings)

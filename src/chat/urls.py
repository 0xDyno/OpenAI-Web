from django.urls import path

from . import views

urlpatterns = [
    path(r"chat/", views.ai_page, name="chat"),
]

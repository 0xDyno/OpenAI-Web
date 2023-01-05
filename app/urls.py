from django.urls import path
from . import views


urlpatterns = [
    path("", views.intro, name="home"),
    path("chat/", views.chat_gpt_page, name="chat"),
    path("generate/", views.generate_page, name="generate"),
]
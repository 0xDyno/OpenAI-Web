from django.urls import path
from . import views


urlpatterns = [
    path(r"", views.intro, name="home"),
    path(r"chat/", views.chat_gpt_page, name="chat"),
    
    path(r"generate/", views.generate_page, name="generate"),
    path(r"generate/variate/<path:url>", views.generate_variation_page, name="variate"),
    path(r"generate/save/<path:url>", views.save_img, name="save"),
    path(r"generate/increase/<path:url>", views.increase_page, name="increase"),
    
    path(r"magic/", views.magics_page, name="magic"),
    path(r"magic/<int:pk>/", views.magics_item_page, name="magic_item"),
]
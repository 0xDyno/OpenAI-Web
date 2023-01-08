from django.urls import path
from . import views


urlpatterns = [
    path("", views.intro, name="home"),
    path("chat/", views.chat_gpt_page, name="chat"),
    
    path("generate/", views.generate_page, name="generate"),
    path("generate/save/<str:size>/<path:url>/", views.save_img, name="save"),
    path("generate/variate/<str:size>/<path:url>/", views.generate_variation_page, name="variate"),
    
    path("magic/", views.magics_page, name="magic"),
    path("magic/<int:pk>/", views.magics_item_page, name="magic_item"),
]
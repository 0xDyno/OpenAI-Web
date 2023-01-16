from django.urls import path

from . import views

urlpatterns = [
    path(r"chat/", views.ai_page, name="chat"),
    path(r"chat/history/", views.all_history, name="all_history"),
    path(r"chat/delete/<int:pk>", views.delete, name="delete"),
    
]

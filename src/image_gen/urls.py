from django.urls import path

from . import views

urlpatterns = [
    path(r"image_generator/", views.ai_page, name="image_generator"),
    
    path(r"image_generator/variate/<path:url>/<str:prompt>/<int:size>/<int:amount>/", views.variate, name="variate"),
    path(r"image_generator/save/<path:url>/<str:prompt>/<int:size>/", views.save_page, name="save"),
    path(r"image_generator/increase/<path:url>/<str:prompt>/<int:size>/", views.resolution_page, name="increase"),
    
    path(r"gallery/", views.gallery_page, name="gallery"),
    path(r"gallery/image/<int:pk>/", views.image_page, name="gallery_image"),
    path(r"image_generator/download/<path:url>/<str:prompt>/<int:size>/", views.download_page, name="download"),
]

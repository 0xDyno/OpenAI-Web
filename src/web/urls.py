from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from . import views_generate

urlpatterns = [
    path(r"", views.home, name="home"),
    path(r"login/", auth_views.LoginView.as_view(template_name="main/login_page.html"), name="login"),
    path(r"profile/", views.settings_page, name="profile"),
    path(r"signup/", views.signup_page, name="signup"),
    path(r"signout/", auth_views.LogoutView.as_view(), name="signout"),
    
    
    path(r"chat/", views.chat_ai_view, name="chat_ai"),
    path(r"chat/<int:chat_id>/", views.chat_ai_conversation_view, name="chat_ai_conversation"),
    path(r"chat/delete/<int:chat_id>", views.delete_chat_view, name="delete_chat"),
    path(r"text/", views.text_ai_view, name="text_ai"),
    path(r"text/history/", views.chat_history_view, name="text_history"),
    path(r"text/delete/<int:pk>", views.delete_conversation_view, name="delete_conversation"),
    
    
    path(r"image_generator/", views_generate.ai_page, name="ig_ai"),
    
    path(r"image_generator/variate/<path:url>/<str:prompt>/<int:size>/<int:amount>/",
         views_generate.variate_url, name="variate_url"),
    path(r"image_generator/variate/<int:pk>/", views_generate.variate_img, name="variate_img"),
    path(r"image_generator/save/<path:url>/<str:prompt>/<int:size>/", views_generate.save_page, name="save_img"),
    path(r"image_generator/increase/<path:url>/<str:prompt>/<int:size>/", views_generate.resolution_page,
         name="increase_img"),
    
    path(r"gallery/", views_generate.gallery_page, name="gallery"),
    path(r"gallery/image/<int:pk>/", views_generate.image_page, name="gallery_img"),
    path(r"gallery/image/delete/<int:pk>/", views_generate.delete_image_page, name="delete_img"),
    path(r"gallery/download/<path:url>/<str:prompt>/<int:size>/", views_generate.download_page, name="download_img"),
]

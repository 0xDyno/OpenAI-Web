from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(r"", views.home, name="home"),
    path(r"login/", auth_views.LoginView.as_view(template_name="login_page.html"), name="login"),
    path(r"profile/", views.settings_page, name="profile"),
    
    path(r"signup/", views.signup_page, name="signup"),
    path(r"signout/", auth_views.LogoutView.as_view(), name="signout"),
]

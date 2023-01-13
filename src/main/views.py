from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from .forms import SettingsFrom
from .models import Settings

# Create your views here.


def home(request):
    return render(request=request, template_name="home.html")


def signup_page(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            Settings(user=user).save()
            
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your profile was successfully created! Log in here:")
            
            return settings_page(request)
        else:
            messages.error(request, form.error_messages)
    
    context = {"form": UserCreationForm()}
    return render(request=request, template_name="signup.html", context=context)


def settings_page(request):
    if not request.user.is_authenticated:
        return not_authenticated(request)
    
    if request.method == "POST":
        form = SettingsFrom(request.POST)
        if form.is_valid():
            settings = Settings.objects.get(user=request.user)
            new_key = form.cleaned_data.get("openai_key")
            
            if settings.openai_key != new_key:
                settings.openai_key = new_key
            
            settings.openai_key = form.cleaned_data.get("openai_key")
            settings.save()
            messages.success(request, "Changes successfully saved.")
        else:
            messages.error(request, "Error happened, data is not saved. Please try again.")
    
    user_settings = Settings.objects.get(user=request.user)
    form = SettingsFrom(initial={"openai_key": user_settings.openai_key})
    
    context = {"form": form}
    return render(request=request, template_name="settings.html", context=context)
    

def not_authenticated(request):
    return render(request=request, template_name="not_authenticated.html")

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render

from .forms import ChatGPTForm
from .forms import SettingsFrom
from .models import Conversation
from .models import Settings
from .utils import get_answer

DEF_INITIAL_CHAT = {"model": ChatGPTForm.MODELS[0], "accuracy": 100}


def home(request):
    return render(request=request, template_name="main/home.html")


def signup_page(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            Settings.objects.create(user=user)
            
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your profile was successfully created! Log in here:")
            
            return home(request)
        else:
            messages.error(request, form.error_messages)
    
    context = {"form": UserCreationForm()}
    return render(request=request, template_name="main/signup.html", context=context)


@login_required
def settings_page(request):
    if request.method == "POST":
        form = SettingsFrom(request.POST)
        if form.is_valid():
            settings = Settings.objects.get(user=request.user)
            new_key = form.cleaned_data.get("openai_key")
            
            if settings.openai_key != new_key:
                settings.openai_key = new_key
            
            settings.save()
            messages.success(request, "Changes successfully saved.")
        else:
            messages.error(request, "Error happened, data is not saved. Please try again.")
    
    user_settings = Settings.objects.get(user=request.user)
    form = SettingsFrom(initial={"openai_key": user_settings.openai_key})
    
    context = {"form": form}
    return render(request=request, template_name="main/settings.html", context=context)


###########
# Chat AI #
###########


@login_required
def chat_ai_view(request):
    context = {}
    history = list(Conversation.objects.filter(user=request.user))[-5:]
    if history:
        history.reverse()
        context["history"] = history
    
    if request.method == "POST":
        form = ChatGPTForm(request.POST)
        
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            model = form.cleaned_data["model"]
            temperature = form.cleaned_data["accuracy"]
            
            key = Settings.objects.get(user=request.user).openai_key
            response = get_answer(key, prompt, model, temperature)
            data = {"form": form,
                    "response": response,
                    "prompt": prompt,
                    "model": model,
                    "accuracy": temperature,
                    }
            context.update(data)
            
            conversation = Conversation(user=request.user, prompt=prompt, response=response,
                                        model=model, accuracy=temperature)
            conversation.save()
            
            return render(request=request, template_name="chat/chat_ai.html", context=context)
    
    form = ChatGPTForm(initial=DEF_INITIAL_CHAT)
    context["form"] = form
    return render(request=request, template_name="chat/chat_ai.html", context=context)


@login_required
def chat_history_view(request):
    context = {}
    history = list(Conversation.objects.filter(user=request.user))
    if history:
        history.reverse()
        context["history"] = history
    else:
        context["message"] = "No history at the moment"
    
    return render(request=request, template_name="chat/all_history.html", context=context)


@login_required
def delete_chat_view(request, pk):
    try:
        to_delete = Conversation.objects.get(user=request.user, pk=pk)
        to_delete.delete()
    finally:
        return HttpResponseRedirect(redirect_to="/chat/")
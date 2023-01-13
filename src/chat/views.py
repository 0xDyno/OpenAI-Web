from django.shortcuts import render

from main.models import Settings
from main.views import not_authenticated

from . import forms
from . import utils

# Create your views here.

DEF_INITIAL_CHAT = {"model": forms.ChatGPTForm.MODELS[0], "accuracy": 100}


def ai_page(request):
    if not request.user.is_authenticated:
        return not_authenticated(request)
    
    if request.method == "POST":
        form = forms.ChatGPTForm(request.POST)
        
        print(f"\n\n\n{form.data} {form.is_valid()}\n\n\n")
        
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            model = form.cleaned_data["model"]
            temperature = form.cleaned_data["accuracy"]
            
            key = Settings.objects.get(user=request.user).openai_key
            context = {"form": form,
                       "response": utils.get_answer(key, prompt, model, temperature),
                       "prompt": prompt,
                       "model": model,
                       "accuracy": temperature,
                       }
            return render(request=request, template_name="chat_ai.html", context=context)
    
    form = forms.ChatGPTForm(initial=DEF_INITIAL_CHAT)
    context = {"form": form}
    return render(request=request, template_name="chat_ai.html", context=context)

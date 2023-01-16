from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.models import Settings

from . import forms
from . import utils
from .models import Conversation

# Create your views here.

DEF_INITIAL_CHAT = {"model": forms.ChatGPTForm.MODELS[0], "accuracy": 100}


@login_required
def ai_page(request):
    context = {}
    history = list(Conversation.objects.filter(user=request.user))
    if history:
        history.reverse()
        context["history"] = history
    
    if request.method == "POST":
        form = forms.ChatGPTForm(request.POST)
        
        print(f"\n\n\n{form.data} {form.is_valid()}\n\n\n")
        
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            model = form.cleaned_data["model"]
            temperature = form.cleaned_data["accuracy"]
            
            
            key = Settings.objects.get(user=request.user).openai_key
            response = utils.get_answer(key, prompt, model, temperature)
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
            
            return render(request=request, template_name="chat_ai.html", context=context)
    
    form = forms.ChatGPTForm(initial=DEF_INITIAL_CHAT)
    context["form"] = form
    return render(request=request, template_name="chat_ai.html", context=context)

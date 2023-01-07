from django.shortcuts import render
from . import forms
from . import models
# Create your views here.



def intro(request):
    return render(request=request, template_name="home.html")


def chat_gpt_page(request):
    form = forms.ChatGPTForm()
    context = {"form": form}
    
    if request.method == "POST":
        form = forms.ChatGPTForm(request.POST)
        if form.is_valid():
            user_request = form.data["request"]
            model = form.data["model"]
            temperature = form.data["temperature"]
            
            response = models.get_gpt_respond(user_request, model, temperature)
            context = {"answer": response, "user_request": user_request}
        
    return render(request=request, template_name="chat_gpt.html", context=context)


def generate_page(request):
    return render(request=request, template_name="generate.html")


def magics_page(request):
    return render(request=request, template_name="magic.html")


def magics_item_page(request, pk):
    if pk > 100:
        context = {"message": "404. Not Found"}
    else:
        context = {"message": "Magic things happens here.."}
        
    return render(request=request, template_name="magic_item.html", context=context)

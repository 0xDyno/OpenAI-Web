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
            prompt = form.data["prompt"]
            model = form.data["model"]
            temperature = form.data["temperature"]
            
            response = models.get_answer(prompt, model, temperature)
            context = {"answer": response, "prompt": prompt}
        
    return render(request=request, template_name="chat_gpt.html", context=context)


def generate_page(request):
    form = forms.DalleForm()
    context = {"form": form,
               "amount": 1}
    
    saved_imgs = models.get_saved_imgs()
    if saved_imgs:
        context["gallery"] = saved_imgs
        
    if request.method == "POST":
        form = forms.ChatGPTForm(request.POST)
        if form.is_valid():
            prompt = form.data["prompt"]
            amount = form.data["amount"]
            size = form.data["size"]

            response = models.get_generated_imgs(prompt, int(amount), size)
            context = {"generated": response, "prompt": prompt, "size": size, "amount": amount}
    
    return render(request=request, template_name="generate.html", context=context)


def save_img(request, size, url):
    models.save_image(url)
    return intro(request)


def generate_variation_page(request, size, url):
    form = forms.ChatGPTForm()
    context = {
        "generated": models.variate_image(size, url),
        "form": form,
        "amount": 1,
    }
    return render(request=request, template_name="generate.html", context=context)


def magics_page(request):
    return render(request=request, template_name="magic.html")


def magics_item_page(request, pk):
    if pk > 100:
        context = {"message": "404. Not Found"}
    else:
        context = {"message": "Magic things happens here.."}
        
    return render(request=request, template_name="magic_item.html", context=context)

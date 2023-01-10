from django.shortcuts import render
from . import forms
from . import models
# Create your views here.



def intro(request):
    return render(request=request, template_name="home.html")


def chat_gpt_page(request):
    if request.method == "POST":
        form = forms.ChatGPTForm(request.POST)
        
        print(f"\n\n\n{form.data} {form.is_valid()}\n\n\n")
    
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            model = form.cleaned_data["model"]
            temperature = form.cleaned_data["accuracy"]
        
            context = {"form": form,
                       "response": models.get_answer(prompt, model, temperature),
                       "prompt": prompt,
                       "model": model,
                       "accuracy": temperature,
                       }
            return render(request=request, template_name="chat_gpt.html", context=context)
        
    form = forms.ChatGPTForm(initial={"model": forms.ChatGPTForm.MODELS[0],
                                      "accuracy": 100})
    context = {"form": form}
    return render(request=request, template_name="chat_gpt.html", context=context)


def generate_page(request):
    if request.method == "POST":
        form = forms.DalleForm(request.POST)
        print(f"\n\n\n{form.data} {form.is_valid()}\n\n\n")
    
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            amount = form.cleaned_data["amount"]
            size = form.cleaned_data["size"]
        
            context = {"form": form,
                       "generated": models.get_generated_imgs(prompt, amount, size),
                       "prompt": prompt,
                       "amount": amount,
                       "size": size,
                       }
        
            if "gallery" in form.cleaned_data:
                context["gallery"] = form.cleaned_data["gallery"]
        
            return render(request=request, template_name="generate.html", context=context)
        
    form = forms.DalleForm(initial={"size": forms.DalleForm.SIZES[0],
                           "amount": 1})
    context = {"form": form}
    
    saved_imgs = models.get_saved_imgs()
    if saved_imgs:
        context["gallery"] = saved_imgs

    return render(request=request, template_name="generate.html", context=context)


def save_img(request, size, url):
    models.save_image(url)
    return intro(request)


def generate_variation_page(request, size, url):
    initial = {"size": forms.DalleForm.SIZES[0], "amount": 1}
    
    context = {
        "generated": models.variate_image(size, url),
        "form": forms.DalleForm(initial=initial),
    }
    return render(request=request, template_name="generate.html", context=context)


def magics_page(request):
    context = {"message": "Not ready yet. But magic is coming..."}
    return render(request=request, template_name="magic.html", context=context)


def magics_item_page(request, pk):
    if pk > 100:
        context = {"message": "404. Not Found"}
    else:
        context = {"message": "Magic things happens here.."}
        
    return render(request=request, template_name="magic_item.html", context=context)

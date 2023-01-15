from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Settings
from . import forms
from . import utils
from .models import GeneratedImageModel

# Create your views here.

DEFAULT_VARIATE = 5
DEFAULT_INITIAL = {"size": forms.DalleForm.SIZES[2], "amount": 1}


@login_required
def ai_page(request):
    context = {}
    saved_imgs = utils.get_saved_imgs(request.user)
    if saved_imgs:
        context["gallery"] = saved_imgs
    
    if request.method == "POST":
        form = forms.DalleForm(request.POST)
        print(f"\n\n\n{form.data} {form.is_valid()}\n\n\n")
        
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            amount = form.cleaned_data["amount"]
            size = form.cleaned_data["size"]
            
            key = Settings.objects.get(user=request.user).openai_key
            data = {"form": form,
                    "generated": utils.get_generated_imgs(key, prompt, amount, size),
                    "prompt": prompt,
                    "amount": amount,
                    "size": size,
                    }
            context.update(data)
            return render(request=request, template_name="ai_page.html", context=context)
    
    context["form"] = forms.DalleForm(initial=DEFAULT_INITIAL)
    return render(request=request, template_name="ai_page.html", context=context)


@login_required
def variate(request, url, prompt, size, amount):
    key = Settings.objects.get(user=request.user).openai_key
    initial = {"prompt": prompt, "size": size, "amount": amount}
    context = {"generated": utils.variate_image(key, url, DEFAULT_VARIATE),
               "form": forms.DalleForm(initial=initial)}
    context.update(initial)
    return render(request=request, template_name="ai_page.html", context=context)


@login_required
def save_page(request, url, prompt, size):
    utils.save_image_to_db(request, url, prompt, size)
    return render(request=request, template_name="save.html")


@login_required
def resolution_page(request, url, prompt, size):
    return render(request=request, template_name="resolution.html",
                  context={"result": utils.increase_image_resolution(url), "prompt": prompt, "size": size})


@login_required
def gallery_page(request):
    context = {"message": "Not ready yet. But magic is coming..."}
    return render(request=request, template_name="gallery_page.html", context=context)


@login_required
def download_page(request, url, prompt, size):
    return render(request=request, template_name="download.html",
                  context={"url": url, "prompt": prompt, "size": size})


@login_required
def image_page(request, pk):
    if pk > 100:
        context = {"message": "404. Not Found"}
    else:
        context = {"message": "Magic things happens here.."}
    
    return render(request=request, template_name="image_page.html", context=context)
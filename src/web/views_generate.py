from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse

from . import forms
from . import utils
from .models import GeneratedImageModel
from .models import Settings

DEFAULT_INITIAL = {"size": forms.DalleForm.SIZES[2], "amount": 1}


@login_required
def ai_page(request):
    context = {}
    saved_imgs = utils.get_saved_imgs(request.user, 20)
    if saved_imgs:
        context["gallery"] = saved_imgs
        context["gallery_message"] = "Saved images:"
    
    if request.method == "POST":
        form = forms.DalleForm(request.POST)
        
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
            return render(request=request, template_name="image_gen/ai_page.html", context=context)
    
    context["form"] = forms.DalleForm(initial=DEFAULT_INITIAL)
    return render(request=request, template_name="image_gen/ai_page.html", context=context)


@login_required
def variate_url(request, url, prompt, size, amount):
    key = Settings.objects.get(user=request.user).openai_key
    initial = {"prompt": prompt, "size": size, "amount": amount}
    context = {"generated": utils.variate_image_by_url(key, url),
               "form": forms.DalleForm(initial=initial)}
    context.update(initial)
    return render(request=request, template_name="image_gen/ai_page.html", context=context)


def variate_img(request, pk):
    img = GeneratedImageModel.objects.get(pk=pk)
    
    initial = DEFAULT_INITIAL.copy()
    initial.update({"prompt": img.prompt, "amount": utils.DEFAULT_VARIATE_AMOUNT})
    
    key = Settings.objects.get(user=request.user).openai_key
    context = {
        "generated": utils.variate_image_by_img(key, img.image.name),
        "form": forms.DalleForm(initial=initial),
        "prompt": img.prompt,
        "size": img.resolution,
        "amount": utils.DEFAULT_VARIATE_AMOUNT,
    }
    
    return render(request=request, template_name="image_gen/ai_page.html", context=context)


@login_required
def save_page(request, url, prompt, size):
    utils.save_image_to_db(request, url, prompt, size)
    return render(request=request, template_name="image_gen/save.html")


@login_required
def resolution_page(request, url, prompt, size):
    return render(request=request, template_name="image_gen/resolution.html",
                  context={"result": utils.increase_image_resolution(url), "prompt": prompt, "size": size})


@login_required
def gallery_page(request):
    gallery = utils.get_saved_imgs(request.user)
    if gallery:
        context = {
            "gallery_message": "Wow, you have wonderful collection!",
            "gallery": gallery,
        }
    else:
        context = {"message": "Nothing is here... But magic is coming! Try Dall-E"}
    return render(request=request, template_name="image_gen/gallery_page.html", context=context)


@login_required
def download_page(request, url, prompt, size):
    return render(request=request, template_name="image_gen/download.html",
                  context={"url": url, "prompt": prompt, "size": size})


@login_required
def image_page(request, pk):
    image = get_object_or_404(GeneratedImageModel, pk=pk)
    
    if image.user != request.user and not request.user.is_superuser:
        messages.error(request, message="This is private picture, you don't have permissions to delete it")
        return render(request=request, template_name="image_gen/image_page.html")
    
    context = {"image": image, "size": utils.get_resolution(image.resolution)}
    return render(request=request, template_name="image_gen/image_page.html", context=context)


@login_required
def delete_image_page(request, pk):
    image = get_object_or_404(GeneratedImageModel, pk=pk)
    
    if image.user != request.user and not request.user.is_superuser:
        messages.error(request, message="This is private picture, you don't have permissions to delete it")
        return render(request=request, template_name="image_gen/image_page.html")
    
    image.delete()
    return HttpResponseRedirect(reverse("gallery"))

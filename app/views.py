from django.shortcuts import render

# Create your views here.


def intro(request):
    return render(request=request, template_name="home.html")


def chat_gpt_page(request):
    return render(request=request, template_name="chat_gpt.html")


def generate_page(request):
    return render(request=request, template_name="generate.html")

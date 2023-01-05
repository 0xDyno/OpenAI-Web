from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def intro(request):
    return render(request=request, template_name="home.html")


def chat_gpt_page(request):
    return HttpResponse("Talk with ChatGPT")


def generate_page(request):
    return HttpResponse("Generate image")

from django.shortcuts import render

# Create your views here.

context = {
    "title": "AI Interface",
}


def intro(request):
    return render(request=request, template_name="home.html", context=context)


def chat_gpt_page(request):
    context_gpt = context.copy()
    if request.method == "POST":
        context_gpt["answer"] = "something"
        
    return render(request=request, template_name="chat_gpt.html", context=context_gpt)


def generate_page(request):
    return render(request=request, template_name="generate.html", context=context)


def magics_page(request):
    return render(request=request, template_name="magic.html", context=context)


def magics_item_page(request, pk):
    if pk > 100:
        mip_context = {"message": "404. Not Found"}
    else:
        mip_context = {"message": "Magic things happens here.."}
        
    mip_context.update(context)
    return render(request=request, template_name="magic_item.html", context=mip_context)

from threading import Thread

import openai as ai

import requests

from django.core.files.base import ContentFile

from image_gen.models import ImageModel
from main.utils import load_openai_key


@load_openai_key
def get_generated_imgs(prompt, number, size):
    match size:
        case "1":
            size = "1024x1024"
        case "2":
            size = "512x512"
        case "3":
            size = "256x256"
        case "_":
            size = "1024x1024"
    
    number = 1 if number < 1 or number > 10 else number
    
    try:
        response = ai.Image.create(prompt=prompt, n=number, size=size)
    except (ai.InvalidRequestError, ai.error.RateLimitError) as error:
        return [error.error["message"]]
    except ai.OpenAIError:
        return ["Sorry, unknown error happened. Try again later or contact support."]
    
    urls = [data["url"] for data in response['data']]
    return urls


@load_openai_key
def variate_image(url, amount):
    image = requests.request(url=url, method="GET").content
    size = "256x256"
    
    try:
        response = ai.Image.create_variation(image=image, n=amount, size=size)
    except (ai.InvalidRequestError, ai.error.RateLimitError) as error:
        return [error.error["message"]]
    except ai.OpenAIError:
        return ["Sorry, unknown error happened. Try again later or contact support."]
    
    urls = [data["url"] for data in response['data']]
    return urls


def increase_image_resolution(url: str):
    return "Here should be 1 increased photo, full size for:\n{}\n " \
           "But it's not ready, sorry..".format(url)


def get_saved_imgs():
    return list()


def save_image_to_db(request, url, prompt, size):
    def work():
        r = requests.request(url=url, method="GET")
        content = ContentFile(r.content)
        name = get_img_name_from_url(url)
    
        db_image = ImageModel(user=request.user, prompt=prompt, resolution=size)
        db_image.image.save(name=name, content=content)
        db_image.save()
    
    thread = Thread(target=work)
    thread.start()


def get_img_name_from_url(url: str):
    for part in url.split("/"):
        if part.startswith("img"):
            return part.split("?")[0]
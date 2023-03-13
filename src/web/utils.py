from datetime import datetime
from os import getenv
from threading import Thread

import openai as ai
import requests
from django.core.files.base import ContentFile
from dotenv import load_dotenv

from .models import GeneratedImageModel

load_dotenv(dotenv_path="config/.env")


def load_openai_key(func):
    """
    Uses first argument as OpenAI API key and then call functions with all other vars
    After the work - deletes API
    """
    def wrapper(*args):
        ai.api_key = args[0]
        result = func(*args[1:])
        ai.api_key = ""
        return result
    return wrapper


###########
# Chat AI #
###########


@load_openai_key
def get_answer(prompt, model, temp):
    if model == getenv("DAVINCI3"):
        max_tokens = 3500
    elif model == getenv("DAVINCI2"):
        max_tokens = 3000
    else:
        max_tokens = 2000
    
    try:
        response = ai.Completion.create(model=model, prompt=prompt,
                                        temperature=convert_temp(temp), max_tokens=max_tokens)
        return response.choices[0].text
    except (ai.InvalidRequestError, ai.error.RateLimitError) as error:
        return f"Error: {error.error['message']}"
    except ai.error.AuthenticationError as error:
        return f"Error: {error.error['message']}" + "\n\nYou can setup your keys in your Profile's settings"
    except ai.OpenAIError:
        return "Sorry, unknown error happened. Try again later or contact support."


def convert_temp(temp):
    """from 100 to 1 & 1 to 0.01, also checks it"""
    if temp > 100:
        temp = 100
    if temp < 0:
        temp = 0
    return temp / 100


############
# Generate #
############


DEFAULT_VARIATE_AMOUNT = 5
DEFAULT_GENERATE_SIZE = "256x256"


@load_openai_key
def get_generated_imgs(prompt, number, size):
    size = get_resolution(size)
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
def variate_image_by_url(url, amount: int = DEFAULT_VARIATE_AMOUNT, size: str = DEFAULT_GENERATE_SIZE):
    image = requests.request(url=url, method="GET").content
    
    try:
        response = ai.Image.create_variation(image=image, n=amount, size=size)
    except (ai.InvalidRequestError, ai.error.RateLimitError) as error:
        return [error.error["message"]]
    except ai.OpenAIError:
        return ["Sorry, unknown error happened. Try again later or contact support."]
    
    urls = [data["url"] for data in response['data']]
    return urls


@load_openai_key
def variate_image_by_img(path, amount: int = DEFAULT_VARIATE_AMOUNT, size: str = DEFAULT_GENERATE_SIZE):
    with open(path, "rb") as r:
        img_bytes = r.read()
    
    try:
        response = ai.Image.create_variation(image=img_bytes, n=amount, size=size)
    except (ai.InvalidRequestError, ai.error.RateLimitError) as error:
        return [error.error["message"]]
    except ai.OpenAIError:
        return ["Sorry, unknown error happened. Try again later or contact support."]
    urls = [data["url"] for data in response['data']]
    return urls


def increase_image_resolution(url: str):
    return "Here should be 1 increased photo, full size for:\n{}\n " \
           "But it's not ready, sorry..".format(url)


def get_saved_imgs(user, number=500) -> list:
    """Return format -> list with dicts:
    [
        {
            "date": date,
            "size": last_size,
            "prompt": last_prompt,
            "images": ["images/some_chars.png", "url_2", "url_3", "url_4"],
        },
        {"size": last_size, "prompt": last_prompt, "date": date, "images": [list with urls]},
        {"size": last_size, "prompt": last_prompt, "date": date, "images": [list with urls]},
        {"size": last_size, "prompt": last_prompt, "date": date, "images": [list with urls]},
    ]
    """
    raw = list(GeneratedImageModel.objects.filter(user=user))
    raw = raw[-number:] if number else raw
    
    result = divide_by_prompt(raw, [])
    return result


def divide_by_prompt(raw: list, result: list, current_dict: dict = None,
                     last_prompt: str = None, last_size: int = None) -> list:
    """
    Function serves goal to divide images to sets with the save prompt & size.

    Recursion. If we have elements in raw - get last, delete from the list.
        If last_prompt != current prompt - that means it's first iteration or end for old dict. We need to check it...
    if we have elements in current_dict - save info fist. Then init - last info, date, current_dict etc..
        If last_prompt == current prompt - that element should be in current_dict, append and move on again to recursion
    """
    if raw:
        img = raw.pop()
        
        if last_prompt == img.prompt and img.resolution == last_size:
            current_dict["images"].append(img)
            return divide_by_prompt(raw, result, current_dict, last_prompt, last_size)
        else:
            if current_dict:
                result.append(current_dict)
            
            last_size = img.resolution
            last_prompt = img.prompt
            date = datetime.date(img.created).strftime("%d-%m-%Y")
            current_dict = {
                "size": get_resolution(img.resolution),
                "prompt": last_prompt,
                "date": date,
                "images": [img],
            }
            return divide_by_prompt(raw, result, current_dict, last_prompt, last_size)
    else:
        if current_dict:
            result.append(current_dict)
        return result


def get_resolution(number):
    match number:
        case "1":
            return "1024x1024"
        case "2":
            return "512x512"
        case "3":
            return "256x256"
        case _:
            return "Unknown"


def save_image_to_db(request, url, prompt, size):
    def work():
        r = requests.request(url=url, method="GET")
        content = ContentFile(r.content)
        name = get_img_name_from_url(url)
        path = "images/" + name
        
        db_image = GeneratedImageModel(user=request.user, prompt=prompt, resolution=size, path=path)
        db_image.image.save(name=name, content=content)
        db_image.save()
    
    thread = Thread(target=work)
    thread.start()


def get_img_name_from_url(url: str):
    """type should be                 star -> img_name_efwef.png <- end
    https://any-domain.com/?any-sign-gesg&anyHimg_name_efwef.png?end_this_part_wont_be_added=fefwef..               """
    for part in url.split("/"):
        if part.startswith("img"):
            return part.split("?")[0]

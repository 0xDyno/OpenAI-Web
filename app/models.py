import os
import random

from django.db import models
import openai as ai
import environ
import requests
from openai import InvalidRequestError
from openai.error import RateLimitError

# Create your models here.
env = environ.Env()
env.read_env("OpenAI_Web/.env")
ai.api_key = env("OPENAI_SECRET_KEY")


def get_answer(prompt, model, temp) -> list:
    try:
        temp = int(temp)
    except TypeError:
        temp = 1
    else:
        temp = 1 if temp < 0 or temp > 1 else temp
        
    if model == env("DAVINCI3"):
        max_tokens = 4000
    elif model == env("DAVINCI2"):
        max_tokens = 8000
    else:
        max_tokens = 2000
        
    try:
        response = ai.Completion.create(model=model, prompt=prompt,
                                        temperature=temp, max_tokens=max_tokens)
        string = response.choices[0].text
    except (InvalidRequestError, RateLimitError) as error:
        string = f"Error: {error.error['message']}"

    return string


def get_generated_imgs(prompt, number, size):
    match size:
        case "1":
            size = "256x256"
        case "2":
            size = "512x512"
        case "3":
            size = "1024x1024"
        case "_":
            size = "256x256"

    number = 1 if number < 1 or number > 10 else number

    from openai import InvalidRequestError
    try:
        response = ai.Image.create(prompt=prompt, n=number, size=size)
    except (InvalidRequestError, RateLimitError) as error:
        return [error.error["message"]]

    urls = [data["url"] for data in response['data']]
    return urls


def save_image(url):
    pass


def variate_image(size, url):
    image = requests.request(url=url, method="GET").content
    size = "1024x1024" if size == "big" else "256x256"
    try:
        response = ai.Image.create_variation(image=image, n=5, size=size)
    except (InvalidRequestError, RateLimitError) as error:
        return [error.error["message"]]
    
    urls = [data["url"] for data in response['data']]
    return urls


def get_saved_imgs():
    return list()
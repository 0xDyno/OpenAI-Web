import os
import random
from time import sleep

from django.db import models
import environ
import requests
from django.http import FileResponse

import openai as ai
from openai import InvalidRequestError
from openai.error import RateLimitError
from openai.error import APIConnectionError

# Create your models here.
env = environ.Env()
env.read_env("AI_Interface/.env")
ai.api_key = env("OPENAI_SECRET_KEY")


def get_answer(prompt, model, temp) -> list:
    temp = 100 if temp > 100 else temp
    temp = 0 if temp < 0 else temp
    temp = temp / 100
    
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
    except (ai.InvalidRequestError, ai.error.RateLimitError) as error:
        string = f"Error: {error.error['message']}"
    except ai.error.APIConnectionError as error:
        string = f"Error: {error.error['message']}"

    return string


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
    except ai.error.APIConnectionError as error:
        return [error.error['message']]

    urls = [data["url"] for data in response['data']]
    return urls


def variate_image(url):
    image = requests.request(url=url, method="GET").content
    size = "256x256"
    
    try:
        response = ai.Image.create_variation(image=image, n=5, size=size)
    except (ai.InvalidRequestError, ai.error.RateLimitError) as error:
        return [error.error["message"]]
    except ai.error.APIConnectionError as error:
        return [error.error['message']]
    
    urls = [data["url"] for data in response['data']]
    return urls


def increase_image_resolution(url: str):
    return "Here should be 1 increased photo, full size for:\n{}\n " \
           "But it's not ready, sorry..".format(url)


def get_saved_imgs():
    return list()
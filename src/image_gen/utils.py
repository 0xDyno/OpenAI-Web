import openai as ai

import requests


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


def variate_image(url):
    image = requests.request(url=url, method="GET").content
    size = "256x256"
    
    try:
        response = ai.Image.create_variation(image=image, n=1, size=size)
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

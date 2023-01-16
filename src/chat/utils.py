from os import getenv

import openai as ai
from dotenv import load_dotenv

from main.utils import load_openai_key
from .models import Conversation


load_dotenv(dotenv_path="config/.env")


@load_openai_key
def get_answer(prompt, model, temp):
    if model == getenv("DAVINCI3"):
        max_tokens = 3500
    elif model == getenv("DAVINCI2"):
        max_tokens = 8000
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

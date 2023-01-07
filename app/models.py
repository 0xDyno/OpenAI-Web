from django.db import models
import openai as ai
import environ

# Create your models here.


def get_gpt_respond(request, model, temp) -> list:
    env = environ.Env()
    env.read_env("OpenAI_Web/.env")
    ai.api_key = env("OPENAI_SECRET_KEY")

    try:
        temp = int(temp)
    except TypeError:
        temp = 1
    else:
        temp = 1 if temp < 0 or temp > 1 else temp
        
    max_tokens = 4000 if model == env("DAVINCI") else 2048
    
    response = ai.Completion.create(model=model, prompt=request, temperature=temp, max_tokens=max_tokens)
    string = response.choices[0].text.split("\n")
    return string.split("\n") if "\n" in string else [string]
import openai as ai


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

import random
import requests
import logging


def wrap_text(text):
    return f" {text} "


def get_logger():
    log_format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename="logfile.log",
        filemode="w",
        format=log_format,
        level=logging.INFO)
    logger = logging.getLogger()
    return logger


# TODO: make async
def get_fresh_quote(quotes: int, return_dict={}):
    result = ""
    for _ in range(quotes):
        quotable_api_url = "https://api.quotable.io/random"  # Don't Abuse the apis :)
        try:
            response = requests.get(quotable_api_url)
        except ConnectionError as cer:
            raise cer
        except Exception as e:
            raise Exception(
                "Could not fetch your typing data !! Sorry for the inconvenience"
            )
        if response.status_code == 200:
            data = response.json()
            quote = data["content"]
            result += quote + " "
        else:
            raise Exception(
                "Could not fetch your typing data !! Sorry for the inconvenience"
            )
    return_dict[quotes] = result[: len(result) - 1]
    return result[: len(result) - 1]  # removes last space


def get_speed_emoticons(speed, accuracy):
    if accuracy<=60:
        return f'Whats less, Vitamin D in your body or your accuracy while typing !!'
    if speed in range(40):
        return random.choice(['🫠', '😶', '🤥', '🫥','😐','😑'])+' '+\
            random.choice(['Long way to go pal !!','Ruko beta abhi bohat kuch seekhna hai jeevan me', 'Is your keyboard on a coffee break, or is it just afraid of getting carpal tunnel from your slow typing speed?'])
    elif speed in range(41, 61):
        return  random.choice(['☕', '👔', '🥱', '😴','🌝','🧐'])+' '+'Basic Mitch !!'
    elif speed in range(61, 80):
        return random.choice(['🥵', '😎', '🤓', '😏','😉','🦸'])+' '+'Faster than your average Joe !!'
    elif speed>=80:
        return f'Hey King you dropped this 👑'


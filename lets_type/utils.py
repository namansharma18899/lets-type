import json
import random
import logging
import urllib3 

http = urllib3.PoolManager()


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
        try:
            response = http.request("GET",
                                    "https://api.quotable.io/random")
        except ConnectionError as cer:
            raise cer
        except Exception as e:
            raise Exception(
                "Could not fetch your typing data !! Sorry for the inconvenience"
            )
        if response.status == 200:
            arr = response.data.decode("utf-8").split('\n')
            for o in arr:
                quote = json.loads(o)['content']
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

